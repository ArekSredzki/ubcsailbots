/* Not all browsers support the following deverloper javascript console
*  debug functions. Therefore, we'll create dummy functions
*  in case the browser doesn't define them
*/
if (!window.console) console = {};
console.log = console.log || function(){};
console.warn = console.warn || function(){};
console.error = console.error || function(){};
console.info = console.info || function(){};

console.info('base.js loaded')

