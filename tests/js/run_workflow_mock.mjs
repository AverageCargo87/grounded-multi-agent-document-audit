// Offline driver for workflow/document-audit.workflow.js.
//
// It runs the real script with mock versions of the Workflow hooks:
// - a role agent (prompt carries "ROLE:", "INPUT_FILE:", "OUTPUT_FILE:") is
//   simulated by `python -m docaudit fake-agent`, which writes the same file a
//   real agent would, then the validate command from the prompt is executed;
// - a build step (prompt carries a <<<CMD ... CMD>>> block) executes that command.
// It records the maximum number of agents running at once.
//
// Usage: node run_workflow_mock.mjs <workflow.js> <workflow_args.json> <stats_out.json>

import { readFileSync, writeFileSync } from 'node:fs'
import { execSync } from 'node:child_process'

const [scriptPath, argsPath, statsPath] = process.argv.slice(2)
const source = readFileSync(scriptPath, 'utf8').replace(/^export const meta\s*=/m, 'const meta =')
const args = JSON.parse(readFileSync(argsPath, 'utf8'))
const python = args.python || 'python'

let active = 0
let maxActive = 0
const calls = []
const phases = []
const logs = []
const errors = []

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

function run(cmd) {
  return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
}

async function agent(prompt, opts = {}) {
  active++
  maxActive = Math.max(maxActive, active)
  calls.push(opts.label || '?')
  try {
    await sleep(10) // let other queued tasks interleave, so the concurrency cap is exercised
    const role = /^ROLE: (.+)$/m.exec(prompt)
    const cmd = /<<<CMD\n([\s\S]*?)\nCMD>>>/.exec(prompt)
    if (role) {
      const input = /^INPUT_FILE: (.+)$/m.exec(prompt)[1].trim()
      const output = /^OUTPUT_FILE: (.+)$/m.exec(prompt)[1].trim()
      const label = output.replace(/^agents\//, '').replace(/\.json$/, '')
      const out = run(`${python} -m docaudit fake-agent --run "${args.runDir}" --role ${role[1].trim()} --label ${label} --input ${input}`)
      const summary = JSON.parse(out.trim().split('\n').pop())
      const valid = run(cmd[1]).trim() === 'OK'
      return { output_path: `${args.runDir}/${output}`, valid, n_items: summary.n_items }
    }
    if (cmd) {
      const out = run(cmd[1])
      return { exit_code: 0, summary_json: out.trim().split('\n').pop() }
    }
    throw new Error('unrecognised agent prompt')
  } finally {
    active--
  }
}

async function parallel(thunks) {
  return Promise.all(thunks.map(t => t().catch(e => { errors.push(String(e)); return null })))
}

async function pipeline(items, ...stages) {
  return Promise.all(items.map(async (item, i) => {
    let r = item
    for (const stage of stages) {
      try { r = await stage(r, item, i) } catch (e) { errors.push(String(e)); return null }
    }
    return r
  }))
}

const phase = title => phases.push(title)
const log = message => logs.push(message)
const budget = { total: null, spent: () => 0, remaining: () => Infinity }

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const body = new AsyncFunction('agent', 'parallel', 'pipeline', 'phase', 'log', 'args', 'budget', 'workflow', source)
let result = null
try {
  result = await body(agent, parallel, pipeline, phase, log, args, budget, null)
} catch (e) {
  errors.push(String(e && e.stack || e))
}
writeFileSync(statsPath, JSON.stringify({ maxActive, calls, phases, logs, errors, result }, null, 2))
process.exit(errors.length ? 1 : 0)
