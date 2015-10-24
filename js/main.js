Vue.config.debug = true;

// build a store that connets the state to the backend
var backendStore = (function ($, Vue, superagent, Plite) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var urls = {
			'status': '/status',
			'tests': '/run-tests',
			'stream': '/stream',
			'files': '/files',
			'download': '/download'
	},
	icons = {
			error: 'icon-cross_mark',
			info: 'icon-information_white'
	},
	module = {
		statusList: [],
		fileList: [],
		hasStatusItems : false,
		hasErrorItems: false,
		streamLink: ''
	};
	// private methods
	var statusListFilter = function (item) {
		return item.status !== 'good';
	},
	statusListErrorFilter = function (item) {
		return item.class === 'error';
	},
	statusListMap = function (item) {
		var icon = icons.error;
		var title = 'Error';

		if(item.status === 'attention') { 
			icon = icons.info;
			title = 'Warning';
		}

		return {
			'class': item.status,
			'icon': icon,
			'message': item.message,
			'title': title
		}
	},
	updateStatusIntervall = function (timeout) {
		module.getStreamStatus()
			.then(
				function success () {
					window.setTimeout(updateStatusIntervall, 2000);
				}
			)
			.catch(
				function error () {
					console.error('error in darkice');
					module.streamLink = '';
				}
			);
	},
	updateStatusList = function updateStatusList (messages) {
		module.statusList = messages.filter(statusListFilter).map(statusListMap);
		module.hasStatusItems = module.statusList.length !== 0;
		module.hasErrorItems = module.statusList.filter(statusListErrorFilter).length !== 0;
	};
	// public methods
	module.init = function () {
		//module.getStatus();
	},
	module.startUpdateStatusIntervall = function ()  {
		updateStatusIntervall(2000);
	}
	module.getStatus = function () {
		var self = this;
		superagent.get(urls.status)
			.end(function (error, response) {
				if(!Boolean(error)) {
					updateStatusList(response.body);
				}
			});
	},
	module.getStreamStatus = function () {
		var p = new Plite();

		superagent
			.get(urls.stream)
			.end(function (error, response) {
				if(!Boolean(error) && response.body && response.body.errors !== 0) {
					updateStatusList(response.body.messages);
					p.reject();
				}
				else {
					p.resolve(response);
				}
			});

		return p;
	},
	module.sendStreamFormData = function (formData) {
		var serializedObject = JSON.stringify(formData);
		var promise = new Plite();

		superagent
			.post(urls.stream)
			.send(formData)
			.end(function (error, response) {
				if(error) {
					promise.reject(error);
				}
				else {
					promise.resolve(response);
				}
				// update status
				updateStatusIntervall(1000);
			});

		return promise;
	},
	module.getDownloadFiles = function () {
		var promise = Plite();

		superagent
			.get(urls.files)
			.end(function getResponse (error, response) {
				if (error) {
					promise.reject(error);
				}
				else {
					console.log(response);
					module.fileList = JSON.parse(response.text);
					console.log(module.fileList);
					promise.resolve();
				}
			});

		return promise;
	},
	module.deleteFile = function (filename) {
		var promise = Plite();

		superagent
			.del(urls.download + '/' + filename)
			.end(function getResponse (error, response) {
				if (error) {
					promise.reject(error);
				}
				else {
					console.log(response);
					promise.resolve();
				}
			});

		return promise;
	},
	module.rerunTests = function () {
		var promise = Plite();

		superagent
			.get(urls.tests)
			.end(function getResponse (error, response) {
				if(error) {
					promise.reject(error);
				}
				else {
					module.statusList = [];
					updateStatusList(response.body);
					promise.resolve();
				}

				console.log(error);
				console.log(response);
			});

		return promise;
	};
	//return the module
	return module;
}(jQuery, Vue, superagent, Plite));

// build two components
// build a function that returns an intial state (global vars are not fun, but in this case its like a user session)
// use the module pattern for the state

var stateFactory = (function ($, backendStore) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module

	// private methods
	var simpleValidator = function () {
		if(this.value != '') return true;
		return false;
	},
	toJSON = function () {
		return this.value;
	},
	makeAelementOutOfString = function (inputString) {
		var aElement;
		if(inputString.indexOf('http://') !== 1 || inputString.indexOf('https://') !== 1) {
			aElement = $('<a />').attr('href', 'http://' + inputString);
		}
		else {
			aElement = $('<a />').attr('href', inputString);
		}

		return aElement;
	},
	simpleUrlValidator = function () {
		var aElement = makeAelementOutOfString(this.value);
		return Boolean(aElement.get(0).hostname);
	};

	// private vars
	var initalState = {
		'isStreaming': false,
		'isValidForm': false,
		'errorList': [],
		'streamLink': '',
		'formData': {
			name: {
				value: '',
				validator: simpleValidator,
				isValid: false,
				toJSON: toJSON
			},
			description: {
				value: '',
				validator: simpleValidator,
				isValid: false,
				toJSON: toJSON
			},
			url: {
				value: 'nonoradio.tumblr.com',
				validator: simpleUrlValidator,
				isValid: false,
				toJSON: function () {
					return makeAelementOutOfString(this.value).get(0).href;
				}
			},
			genre: {
				value: '',
				validator: function () {
					return true;
				},
				isValid: true,
				toJSON: toJSON
			}
		},
		'store': {}
	},
	module = {};
	// public methods
	module.init = function (options) {
		backendStore.init();
		initalState.store = backendStore;
		return $.extend(initalState, options);
	};
	//return the module
	return module;
}(jQuery, backendStore));

var app = (function ($, Vue, superagent) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {};
	// private methods
	// public methods
	module.init = function () {
		var state = stateFactory.init();
		state.store.getStatus();
		// with this state, build the components
		// js pass by ref should be able to update the state inside the components

		var errorListComponent = Vue.extend({
			data: {
				state: state
			},
			'template': $('#errorListTemplate').html(),
			methods: {
				clickTest: function () {
					this.state.urls.status = 'test3';
					console.log(state.urls.status);
				}
			},
			created: function () {
				console.log('i raise master');
				console.log(this.state);
			}
		});

		var streamFormComponent = Vue.extend({
			data: {
				state: state,
				timeout: -1
			},
			template: $('#streamFormTemplate').html(),
			methods: {
				testForm: function () {
					var self = this;
					// add timeout to check values after a while, ca 200 ms or else cancel timeout
					if (self.timeout !== -1) {
						window.clearTimeout(self.timeout);
					}
					this.timeout = window.setTimeout(function () {
						self.validateForm();
					}, 200);
				},
				validateForm: function validateForm () {
					_.forEach(state.formData, function validateForm (element) {
						element.isValid = element.validator();
					});
					state.isValidForm = _.reduce(state.formData, function reduceForm (input, element) {
						if(!element.isValid) {
							return false;
						} 
						return input;
					}, true);
				}
			},
			created: function () {
				console.log('i raise too, master!');
				this.validateForm();
			}
		});

		var streamButtonComponent = Vue.extend({
			'data': {
				state: state
			},
			template: $('#streamButtonTemplate').html(),
			methods: {
				runStream: function () {
					var self = this;
					if (this.state.isFormValid && !state.store.hasErrorItems) { 
						this.state.store.sendStreamFormData(this.state.formData)
							.then(function updateState (response) {
								self.state.store.streamLink = response.body.link;
							})
							.catch(function error (error) {
								console.error(error);
							});
					}

					return;
				}
			},
			created: function () {
				var self = this;
				this.state.store.getStreamStatus()
					.then(function updateState (response) {
						self.state.store.streamLink = response.body.link;
						self.state.store.startUpdateStatusIntervall();
					})
					.catch(function error (error) {
						console.error(error);
					});
				// console.log('the button raises to be clicked!');
			}
		});

		var testButtonComponent = Vue.extend({
			data: {
				state: state
			},
			methods: {
				rerunTests: function () {
					var self = this;
					self.state.statusListLoading = true;
					self.state.store.rerunTests()
						.then(
							function success () {
								window.setTimeout(function () {
									self.state.statusListLoading = false;
								}, 500);
							}
						)
						.catch(
							function error (error) {
								console.log(error);
							}
						);
				}
			},
			template: $('#testButtonTemplate').html()
		});

		var downloadComponent = Vue.extend({
			template: $('#downloadTemplate').html(),
			data: {
				state: state,
				confirmations: {}
			},
			methods: {
				deleteFile: function deleteFile (filename) {
					var self = this;

					if(this.confirmations[filename] === false) {
						this.confirmations[filename] = true;
						return;
					}
					else if (this.confirmations[filename] === true) {
						state.store.deleteFile(filename)
							.then(self.update())
							.catch(function (error) {
								console.log(error);
							})
					}
					// test comment
				},
				update: function updateMe () {
					var self = this;
					state.store.getDownloadFiles()
					.then(function () {
						for (var i = state.store.fileList.length - 1; i >= 0; i--) {
							self.confirmations.$add(state.store.fileList[i], false);
						};
					});
				}
			},
			created: function created () {
				'use strict';
				this.update();
			}
		});

		Vue.component('error-list', errorListComponent);
		Vue.component('stream-form', streamFormComponent);
		Vue.component('stream-button', streamButtonComponent);
		Vue.component('test-button', testButtonComponent);
		Vue.component('download-list', downloadComponent);

		var mainApp = new Vue({
			el: '#app',
			data: {
				'state': state,
				'showDownloads': false,
			},
			components: {
				'errorList': errorListComponent,
				'streamForm': streamFormComponent,
				'streamButton': streamButtonComponent,
				'testButton': testButtonComponent,
				'download': downloadComponent
			},
			methods: {
				toggleDownloads: function (event) {
					
				}
			},
			created: function () {
				console.log('main app init');
			}
		});
	};
	//return the module
	return module;
}(jQuery, Vue, superagent));


$(document).ready(function(){
	//piStream.init();
	app.init();
	$(document).scrollTop(0);
})