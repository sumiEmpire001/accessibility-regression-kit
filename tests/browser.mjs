import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url),files={'/':['index.html','text/html'],'/index.html':['index.html','text/html'],'/styles.css':['styles.css','text/css'],'/TESTING.md':['TESTING.md','text/plain']};
const server=createServer(async(req,res)=>{const file=files[new URL(req.url,'http://localhost').pathname];if(!file){res.writeHead(404);res.end();return;}try{res.setHeader('Content-Type',file[1]);res.end(await readFile(new URL(file[0],root)));}catch{res.writeHead(500);res.end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base=`http://127.0.0.1:${server.address().port}`,browser=await chromium.launch(),page=await browser.newPage();
await mkdir(new URL('../artifacts/',import.meta.url),{recursive:true});
const results=[];
async function test(name,run){try{await page.goto(base);await run();results.push({name,passed:true});console.log('PASS '+name);}catch(error){results.push({name,passed:false,error:String(error)});console.error('FAIL '+name+' '+error);await page.screenshot({path:new URL('../artifacts/failure-'+results.length+'.png',import.meta.url).pathname,fullPage:true});}}
try{
 await test('keyboard skip link reaches main',async()=>{await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').textContent(),'Skip to main content');await page.keyboard.press('Enter');assert.equal(await page.locator(':focus').getAttribute('id'),'main');});
 await test('native disclosure opens and closes',async()=>{const control=page.getByText('What can I do without a mouse?',{exact:true});await control.click();assert.equal(await page.locator('details').first().getAttribute('open'),'');await control.click();assert.equal(await page.locator('details').first().getAttribute('open'),null);});
 await test('checkbox works with keyboard',async()=>{const check=page.locator('#check-focus');await check.focus();await page.keyboard.press('Space');assert.equal(await check.isChecked(),true);});
 await test('dark theme changes real computed colors',async()=>{await page.locator('#theme-dark').check();assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(16, 32, 26)');await page.locator('#theme-light').check();assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(244, 243, 238)');});
 await test('empty form is blocked by native validation',async()=>{await page.getByRole('button',{name:'Validate practice form'}).click();assert.equal(await page.locator('#sample-name').evaluate(el=>el.validity.valueMissing),true);assert.equal(new URL(page.url()).search,'');});
 await test('invalid email is rejected',async()=>{await page.locator('#sample-name').fill('Synthetic person');await page.locator('#sample-email').fill('invalid');assert.equal(await page.locator('#sample-email').evaluate(el=>el.validity.typeMismatch),true);});
 await test('valid sample navigates to a local query URL',async()=>{await page.locator('#sample-name').fill('Synthetic person');await page.locator('#sample-email').fill('demo@example.invalid');await page.getByRole('button',{name:'Validate practice form'}).click();await page.waitForURL(url=>url.searchParams.get('sample_name')==='Synthetic person');assert.equal(new URL(page.url()).origin,base);});
 await test('reduced motion removes button transition',async()=>{await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.locator('.button').first().evaluate(el=>getComputedStyle(el).transitionDuration),'0s');await page.emulateMedia({reducedMotion:'no-preference'});});
 for(const width of [320,390,768,1280])await test('responsive layout '+width+'px',async()=>{await page.setViewportSize({width,height:900});const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1);assert.equal(overflow,false);await page.screenshot({path:new URL('../artifacts/fieldwork-'+width+'.png',import.meta.url).pathname,fullPage:true});});
}finally{await writeFile(new URL('../artifacts/browser-results.json',import.meta.url),JSON.stringify(results,null,2));await browser.close();await new Promise(resolve=>server.close(resolve));}
if(results.some(result=>!result.passed))process.exitCode=1;
