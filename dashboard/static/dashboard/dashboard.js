var summary = JSON.parse(summaryJSON.replace(/&quot;/g, '"'));
var costPerResult = JSON.parse(CPRJSON.replace(/&quot;/g, '"'));
var summaryPerMonth = JSON.parse(summaryPMJSON.replace(/&quot;/g, '"'));
var topCPO = JSON.parse(topCPOJSON.replace(/&quot;/g, '"'));
var simpleCampaign = JSON.parse(simpleCampaignJSON.replace(/&quot;/g, '"'));

platform = platform.split(",");
multiple_selector = multiple_selector.split(",");

const platform_range = Object.keys(summary.pid).length;
const objective_range = Object.keys(costPerResult.objective).length;
const top_range = Object.keys(topCPO.cid).length;

construct_table(summary, "db1", platform_range, "a");
construct_table(costPerResult, "db2", objective_range, "b");
construct_table(getTopCostPerResult(topCPO, single_selector), "db3", top_range, "c");

function initParams() {
	document.getElementById("startdate").value = startdate;
	document.getElementById("enddate").value = enddate;
	fillCheckboxPlatform("platform-query", platform);
	fillRadio("single-selector", single_selector);
	fillCheckbox("multiple-selector", multiple_selector);

	document.getElementById("topCPO-th").innerHTML = `Cost/<br>${capitalizeFirstLetter(single_selector)}`;
}
initParams();

function capitalizeFirstLetter(string) {
	return string
		.toLowerCase()
		.split("_")
		.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
		.join(" ");
}

// function highlightCostPerResult(table_code) {
// 	for (let i = 0; i < objective_range; i++) {
// 		var objective = costPerResult.objective[i];
// 		if (objective == "reach") {
// 			document.getElementById(`${table_code}-${i}-2`).classList.add("cell-highlight");
// 			document.getElementById(`${table_code}-${i}-3`).classList.add("cell-highlight");
// 		}
// 	}
// }

function fillCheckboxPlatform(groupName, arr) {
	var checkedBoxes = document.querySelectorAll(`input[name=${groupName}]`);

	for (let i = 0; i < checkedBoxes.length; i++) {
		if (!arr.includes((i + 1).toString())) {
			checkedBoxes[i].checked = false;
		}
	}
}

function fillCheckbox(groupName, arr) {
	var checkedBoxes = document.querySelectorAll(`input[name=${groupName}]`);
	for (let i = 0; i < checkedBoxes.length; i++) {
		if (arr.includes(checkedBoxes[i].id)) {
			checkedBoxes[i].checked = true;
		}
	}
}

function fillRadio(groupName, target) {
	var radios = document.querySelectorAll(`input[name=${groupName}]`);

	for (let i = 0; i < radios.length; i++) {
		if (radios[i].id == target) {
			radios[i].checked = true;
		}
	}
}

function getTopCostPerResult(cpo, target) {
	pos_target = ["reach", "impression", "engagement"];
	if (pos_target.includes(target)) {
		target = "costper" + target;
		return construct_ranking_object(cpo, ["name", target]);
	}
	return {};
}

function construct_ranking_object(json_obj, cols) {
	var s_obj = {};

	var top = Object.keys(json_obj[cols[0]]).length;

	var rank_obj = {};
	for (let i = 0; i < top; i++) {
		rank_obj[i] = i + 1;
	}

	s_obj["rank"] = rank_obj;

	for (let i = 0; i < cols.length; i++) {
		s_obj[cols[i]] = json_obj[cols[i]];
	}

	return s_obj;
}

function construct_table(data_object, element_id, range, table_code) {
	var str = "";
	for (let i = 0; i < range; i++) {
		str += construct_row(data_object, i, table_code);
	}
	document.getElementById(element_id).innerHTML = str;
}

function construct_row(data_object, num, table_code) {
	var str = `<tr>`;
	let col = 0;
	for (const [key, value] of Object.entries(data_object)) {
		let cell;
		if (value[num] === null || value[num] === undefined) {
			cell = "";
		} else if (typeof value[num] == "number") {
			cell = Math.round(value[num] * 1000) / 1000;
		} else {
			cell = value[num];
		}
		str += `<td id="${table_code}-${num}-${col}">${cell}</td>`;
		col++;
	}
	return str;
}

function getListCheckedBox(groupName) {
	var checkedBoxes = document.querySelectorAll(`input[name=${groupName}]:checked`);
	var arr = [];
	for (let i = 0; i < checkedBoxes.length; i++) {
		arr.push(checkedBoxes[i].id);
	}
	return arr;
}

function testbutton() {
	console.log(getListCheckedBox("platform-query").toString());
}

function arrayToQueryString(arr) {
	var query_str = "(";
	for (let i = 0; i < arr.length; i++) {
		query_str = query_str + "'" + arr[i] + "'";
		if (i != arr.length - 1) {
			query_str = query_str + ",";
		}
	}
	query_str = query_str + ")";
	return query_str;
}

function createWarning(msg, target_div) {
	var target = document.getElementById(target_div);
	warning = `<div class="alert alert-warning alert-dismissible fade show" role="alert"><i class="bi bi-exclamation-triangle-fill"></i> <b>คำเตือน:</b> ${msg}  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
	target.innerHTML += warning;
}

function queryClear() {
	window.location.href = `/`;
}

function querySubmit() {
	startdate = document.getElementById("startdate").value;
	enddate = document.getElementById("enddate").value;
	platform = getListCheckedBox("platform-query").toString();
	if (document.querySelector('input[name="single-selector"]:checked') == null) {
		single_selector = "";
	} else {
		single_selector = document.querySelector('input[name="single-selector"]:checked').id;
	}
	multiple_selector = getListCheckedBox("multiple-selector").toString();

	let ref = "/?";
	if (startdate != "") {
		ref = ref + `&startdate=${startdate}`;
	}
	if (enddate != "") {
		ref = ref + `&enddate=${enddate}`;
	}
	if (platform != "") {
		ref = ref + `&platform=${platform}`;
	}
	if (single_selector != "") {
		ref = ref + `&ss=${single_selector}`;
	}
	if (multiple_selector != "") {
		ref = ref + `&ms=${multiple_selector}`;
	}
	ref = ref.substring(0, 2) + ref.substring(3);

	// window.location.href = `/?startdate=${startdate}&enddate=${enddate}&platform=${platform}&ss=${single_selector}`;
	window.location.href = ref;
}
