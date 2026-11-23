// SYNTHETIC data. Headless click-through (~5s): loads the page, expands a row, records a fix, names a mistake, re-ranks, switches tab, checks phone width. Run: node check_mvp.js
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const srv = http.createServer((q, res) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, body) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': 'text/html' }); res.end(body); }); });
(async () => {
  await new Promise(ok => srv.listen(0, ok)); const browser = await chromium.launch(); const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && !/fonts\.(googleapis|gstatic)/.test(m.location().url || '') && errs.push(m.text()));
  const t = (label, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + label); if (!ok) errs.push(label); }, txt = s => p.textContent(s);
  await p.goto(`http://localhost:${srv.address().port}/build/mvp.html`); await p.waitForSelector('body[data-ready="1"]');
  t('users are the PM and team leads; synthetic data labelled', (await txt('#header')).includes('The PM for the claims platform and the claims team leads') && (await txt('#title')).includes('Synthetic data'));
  t('three numbers: 55, £68,714, 14', (await txt('#kOver')) === '55' && (await txt('#kGbp')) === '£68,714' && (await txt('#kDen')) === '14');
  const k = await txt('#kpis'); t('each number is explained, delayed split into fraud flags and information requests', k.includes('would have cost if the handler had done what the AI said') && k.includes('fraud flag (£8,739)') && k.includes('request for information (£4,986)') && k.includes('The AI said Deny'));
  t('needs a team lead: 10 overrides, explained', (await txt('#notice')).includes('10 overrides (£11,281)') && (await txt('#notice')).includes('a team lead names it'));
  const lg = await txt('#legend'); t('legend: fix status by hand, repeats counted, weekly bars labelled', lg.includes('entered by you') && lg.includes('counted from overrides received after the fix date') && lg.includes('Overrides per week, 3 Aug to 9 Nov (15 weeks)'));
  t('first row is missed cover, with its claim types', (await p.$$eval('.row', rs => rs[0].dataset.id)) === 'cover' && (await txt('.row[data-id="cover"] .types')).includes('Commercial property 2'));
  t('fix states: came back 2 times; 0 repeats in 2 weeks', (await txt('.row[data-id="version"] .st')).includes('Came back 2 times') && (await txt('.row[data-id="page2"] .st')).includes('0 repeats in 2 weeks'));
  await p.click('.row[data-id="cover"]'); t('row opens with 5 claims, type and example on each', (await p.$$('.detail.open .cl')).length === 5 && (await txt('.detail.open')).includes('Commercial property · '));
  await p.click('.detail.open [data-fix="cover"]'); await p.fill('#fixDate', '2026-08-20');
  t('a fix date before later overrides warns how many count as repeats', (await txt('#fixWarn')).includes('2 overrides received after this date will count as repeats'));
  await p.click('#fixSave'); await p.waitForTimeout(100);
  t('saving the fix shows it by hand and counts 2 repeats', (await txt('.row[data-id="cover"] .st')).includes('Fixed 20 Aug') && (await txt('.row[data-id="cover"] .st')).includes('Came back 2 times') && (await txt('#toast')).includes('2 repeats'));
  await p.click('[data-unfix="cover"]'); t('removing the fix goes back to Not started', (await txt('.row[data-id="cover"] .st')).includes('Not started'));
  await p.click('#openReview'); await p.selectOption('select[data-claim="CLM-1298"]', 'asked'); await p.waitForTimeout(50);
  t('a team lead names one: progress 1 of 10, notice drops to 9', (await txt('#revProgress')).startsWith('1 of 10 named') && (await txt('#notice')).includes('9 overrides'));
  await p.click('#reviewModal [data-close]');
  await p.selectOption('#rankBy', 'denied'); t('rank by valid claims denied: time window second', (await p.$$eval('.row', rs => rs[1].dataset.id)) === 'window');
  await p.click('.tabs button[data-tab="type"]'); t('the existing view by claim type shows six types', (await p.$$('#typeTable tr')).length === 7);
  await p.click('.tabs button[data-tab="mistake"]');
  for (const w of [390, 820]) { await p.setViewportSize({ width: w, height: 900 }); t(`no sideways scrolling at ${w}px`, await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)); }
  t('no errors', errs.length === 0); if (errs.length) console.log(errs);
  await browser.close(); srv.close(); process.exit(errs.length ? 1 : 0);
})();
