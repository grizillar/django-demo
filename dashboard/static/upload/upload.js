var stepper;
var selectedPlatform;
var file;
var additionalDate;
var form = document.getElementById("upload-form");
var addconfig = document.getElementById("config");
var input = document.getElementById("fileinput");

var W1 = document.getElementById("W1");
var E1 = document.getElementById("E1");
var E2 = document.getElementById("E2");
var E3 = document.getElementById("E3");
var E4 = document.getElementById("E4");

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	return new bootstrap.Tooltip(tooltipTriggerEl);
});

// File type
function typeCheck() {
	selectedPlatform = document.querySelector('input[name="type"]:checked').value;
	throwError(E3, false);
	if (selectedPlatform == "GC") {
		addconfig.classList.remove("hidden");
		W1.classList.remove("hidden");
		console.log("Warning: additional config");
	} else {
		addconfig.classList.add("hidden");
		W1.classList.add("hidden");
		document.getElementById("date").value = null;
	}
	if (file) {
		matchCheck();
	}
}

// Drag and drop file upload
let dropArea = document.getElementById("drop-box");
let uploadicon = document.getElementById("upload-icon");

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
	dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
	e.preventDefault();
	e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
	dropArea.addEventListener(eventName, highlight, false);
});
["dragleave", "drop"].forEach((eventName) => {
	dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
	dropArea.classList.add("highlight");
	uploadicon.classList.add("highlight");
}

function unhighlight(e) {
	dropArea.classList.remove("highlight");
	uploadicon.classList.remove("highlight");
}

dropArea.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
	let dt = e.dataTransfer;
	if (dt.files.length > 1) {
		throwError(E1, true);
		console.log("Error: Too many files");
	} else {
		throwError(E1, false);
		input.files = dt.files;
		file = dt.files[0];
		matchCheck();
	}
}

function uploadHandle() {
	file = input.files[0];
	console.log(file);
	throwError(E1, false);
	matchCheck();
}

function matchCheck() {
	let fr = new FileReader();
	fr.onload = csvHandle;
	fr.readAsText(file);

	function csvHandle() {
		let data = fr.result;
		let lines = data.split(/\r?\n/);
		let colLength = lines[0].split(",").length;
		if (selectedPlatform) {
			if (colCheck(colLength, selectedPlatform)) {
				throwError(E2, false);
			} else {
				throwError(E2, true);
				console.log("Error: Not matching file type");
			}
		} else {
			throwError(E3, true);
			console.log("Error: No platform selected");
		}
	}

	function colCheck(col, type) {
		if (col == 10 && type == "GS") {
			return true;
		} else if (col == 20 && type == "FB") {
			return true;
		} else if (col == 44 && type == "LM") {
			return true;
		} else if (col == 15 && type == "LP") {
			return true;
		} else if (col == 17 && type == "GC") {
			return true;
		} else {
			return false;
		}
	}
}

function throwError(Error, mode) {
	if (mode) {
		Error.classList.remove("hidden");
	} else {
		Error.classList.add("hidden");
	}
}

function checkGCDate() {
	additionalDate = document.getElementById("date").value;
	if (additionalDate == "" && selectedPlatform == "GC") {
		throwError(E4, true);
		return false;
	} else {
		throwError(E4, false);
		return true;
	}
}

function submitHandle() {
	if (checkGCDate()) {
		form.submit();
	}
	// if (checkGCDate) {
	// 	form.submit();
	// }
}
