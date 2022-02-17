export {make_request};

const makeCancelable = (promise: Promise<any>) => {
	let hasCanceled_: boolean = false;

	const wrappedPromise: Promise<any> = new Promise((resolve, reject) => {
		promise.then(
			val => hasCanceled_ ? reject({isCanceled: true}) : resolve(val),
			error => hasCanceled_ ? reject({isCanceled: true}) : reject(error)
		);
	});
  
	return {
		promise: wrappedPromise,
		cancel() {
			hasCanceled_ = true;
		},
	};
};

function make_request(method: string, url: string, data: any) {
	return makeCancelable(new Promise(function (resolve, reject) {
		var xhr = new XMLHttpRequest();
		xhr.open(method, url);
		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {
				resolve(xhr.response);
			}
			else {
				reject({
					status: xhr.status,
					statusText: xhr.statusText
				});
			}
		};
		xhr.onerror = function () {
			reject({
				status: xhr.status,
				statusText: xhr.statusText
			});
		};
		xhr.send();
	  }));
}