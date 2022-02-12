import { main_loop } from './loop'

import '@assets/styles/base.css';
import '@assets/styles/icons.css';
import '@assets/styles/main.css';

function main_init() {
    console.log('Hello from js');
    console.log('Create tabs');

    main_loop('init');

    document.getElementById('default_tab')?.click()

    console.log('Do POST');
    const request = new XMLHttpRequest();
    const url = '/api/set/confidence_threshold';
    request.open('POST', url);
    request.setRequestHeader('Content-type', 'application/json');
    var data: object = { key: 'value', deez: 'nutz' };
    var data_str: string = JSON.stringify(data);
    request.send(data_str);
    request.onreadystatechange = (e) => {
        if (request.readyState === 4) {
            console.log(request);
        }
    };
}

let p = new Promise((resolve) => {
    resolve(true);
});
p.then(main_init);

