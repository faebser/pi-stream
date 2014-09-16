var cloner = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		m = Mustache,
		buttons = $('button.root'),
		devs = $('.breadcrumb'),
		cloner = $('#cloner'),
		progress = $('.progress-bar'),
		progressText = $('.progress-text'),
		breadcrumbs = $('.breadcrumb'),
		bar = $('#bar'),
		finish = $('#finish'),
		timeout = 0,
		c = {
			'active': 'active'
		};
	// private methods
	var clickHandler = function () {
		buttons.click(function(event) {
			var e = $(this);
			var parent = e.parents('ol')
			devs.removeClass(c.active);
			parent.addClass(c.active);
			cloner.removeAttr('disabled');
		});
		cloner.click(function(event) {
			var data = {
				'master': '',
				'targets': []
			};
			devs.each(function(index, element) {
				var e = $(element);
				if(e.hasClass(c.active)) {
					data['master'] = e.find('li').first().html();
				}
				else {
					data.targets.push(e.find('li').first().html());
				}
			});
			console.log(data);
			$.ajax({
			    'type': "POST",
			    'url': "clone",
			    'dataType': "json",
			    'data': data
			}).done(function(data) {
				breadcrumbs.fadeOut(400);
				cloner.fadeOut(400, function() {
					updateProgressBar(data.progress);
					bar.fadeIn(700);
					bar.removeClass('hidden');
				});
			});
		});
	},
	updateProgressBar = function (progressData) {
		var percent = parseInt(progressData.split('%')[0].split('[')[1]);
		var css = {};
		if(percent > 0) {
			css = {
				'width': percent + '%',
				'min-width': '20px'
			};
		}
		else {
			css = {
				'width': '0%'
			}
		}
		progress.css(css);
		progress.html(percent + '%'),
		progressText.html(progressData);
		setTheTimeout();
	},
	setTheTimeout = function () {
		timeout = window.setTimeout(function() {
			$.ajax({
				'type': 'GET',
				'url': 'progress',
				'dataType': 'json'
			}).done(function(data) {
				if(data.progress === 'finish') {
					window.clearTimeout(timeout);
					finish.removeClass('hidden');
					finish.fadeIn(400);
					bar.fadeOut(400);
				}
				else {
					updateProgressBar(data.progress);
				}
			})
		}, 1000)
	},
	testForProgress = function () {
		$.ajax({
			'type': 'GET',
			'url': 'progress',
			'dataType': 'json'
		}).done(function(data) {
			if(data.progress !== 0) {
				breadcrumbs.fadeOut(400);
				cloner.fadeOut(400, function() {
					updateProgressBar(data.progress);
					bar.fadeIn(700);
					bar.removeClass('hidden');
				});
				setTheTimeout();
			}
		});
	};
	// public methods
	module.init = function () {
		clickHandler();
		testForProgress();
	};
	//return the module
	return module;
}(jQuery));

$(document).ready(cloner.init());