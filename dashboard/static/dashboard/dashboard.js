var summary = jsonParseQuot(summaryJSON);
var costPerResult = jsonParseQuot(CPRJSON);
var summaryPerMonth = jsonParseQuot(summaryPMJSON);
var platformCount = jsonParseQuot(platformCountJSON);
var possibleYear = jsonParseQuot(possibleYearJSON);

var summaryArray = "";
if (summaryARR) {
	summaryArray = jsonParseQuotArray(summaryARR.split("|"));
}

var summaryByPeriodArray = "";
if (summaryByPeriodARR) {
	summaryByPeriodArray = jsonParseQuotArray(summaryByPeriodARR.split("|"));
}

console.log(summaryByPeriodArray);

// var topCPO = JSON.parse(topCPOJSON.replace(/&quot;/g, '"'));
// var simpleCampaign = jsonParseQuot(simpleCampaignJSON);

// var topCampaign = jsonParseQuot(topCampaignJSON);

// var topCPRarray = [];
// if (topCPRSTR) {
// 	topCPRarray = jsonParseQuotArray(topCPRSTR.split("|"));
// }

platform = platform.split(",");
multiple_selector = multiple_selector.split(",");
period = period.split(",");
year = year.split(",");

page = parseInt(page);

const page_range = year.length;
const platform_range = Object.keys(summary.pid).length;
const platform_count_range = Object.keys(platformCount.pid).length;
const objective_range = Object.keys(costPerResult.objective).length;
// const top_range = Object.keys(topCPRarray[0].cid).length;

var periodArray = [1];
var currently_interval = "date-tab";

const E6 = document.getElementById("E6");
const E7 = document.getElementById("E7");

// Events
const intervalTabs = document.querySelector(".nav-tabs");
intervalTabs.addEventListener("click", (event) => {
	event.preventDefault();
	if (event.target.classList.contains("nav-link")) {
		// Get the ID of the active tab
		const activeTab = intervalTabs.querySelector(".active").getAttribute("id");
		currently_interval = activeTab;
		console.log(currently_interval);
	}
});

construct_table(summary, "db1", platform_range, "a");
construct_table(costPerResult, "db2", objective_range, "b");

function initParams() {
	document.getElementById("startdate").value = startdate;
	document.getElementById("enddate").value = enddate;
	fillCheckboxPlatform("platform-query", platform);
	fillCheckbox("multiple-selector", multiple_selector);

	adjustByTab();
	adjustPeriodArray();

	fillPeriodInput(periodArray);
	pageSet();

	fillCount();
	fillRatioDonut("chart-test-1");

	demoFunction1();

	adjustPageName();

	// document.getElementById("topCPO-th").innerHTML = `Cost/<br>${capitalizeFirstLetter(single_selector)}`;
}
initParams();

// init functions

function demoFunction1() {
	if (by == "date") {
		document.getElementById("summary-per-month-title").innerHTML = "กราฟผลรวม Reach, Impression, Engagementแต่ละเดือน";
	}
	if (by == "period") {
		document.getElementById("summary-per-month-title").innerHTML = "กราฟผลรวม Engagment แต่ละพีเรียด";
	}
}

function adjustPeriodArray() {
	if (page_range > 1) {
		for (let i = 2; i <= page_range; i++) {
			periodArray.push(i);
		}
	}
	document.getElementById("period-counter").innerHTML = periodArray.length;
}

function adjustByTab() {
	if (by == "period") {
		currently_interval = "period-tab";
		document.getElementById("date-tab").classList.remove("active");
		document.getElementById("date-pane").classList.remove("active");
		document.getElementById("period-tab").classList.add("active");
		document.getElementById("period-pane").classList.add("active", "show");
	}
}

function pageSet() {
	if (by != "period") {
		document.getElementById("page-selection").classList.add("hidden");
	}
	// Page boundery
	if (page == 1) {
		document.getElementById("page-dec").classList.add("invisibility");
	}
	if (page == page_range) {
		document.getElementById("page-inc").classList.add("invisibility");
	}
}

function adjustPageName() {
	page_name = document.getElementById("page-name");
	if (period[page - 1] != "") {
		page_name.innerHTML = `หน้าที่ - ${page}: ข้อมูลพีเรียดที่ ${period[page - 1]} ปี ${year[page - 1]}`;
	} else {
		page_name.innerHTML = `หน้าที่ - ${page}: ปี ${year[page - 1]}`;
	}
}

function fillPeriodInput(periodArray) {
	periodArray.forEach((i) => {
		addPeriodInput("period-array", i);
		if (period[i - 1] != "") {
			document.getElementById(`period-filter-${i}`).value = period[i - 1];
		}
		if (year[i - 1] != "") {
			document.getElementById(`year-filter-${i}`).value = year[i - 1];
		}
	});
}

function fillSelect(target_id, arr) {
	var target = document.getElementById(target_id);
	for (let i = 0; i < arr.length; i++) {
		target.innerHTML += `<option value="${arr[i]}">${arr[i]}</option>`;
	}
}

function fillCount() {
	var c_fb = 0;
	var c_ig = 0;
	var c_ln = 0;
	var c_gg = 0;
	for (let i = 0; i < platform_count_range; i++) {
		if (platformCount.pid[i] == "1") {
			c_fb = platformCount.count[i];
		}
		if (platformCount.pid[i] == "2") {
			c_ig = platformCount.count[i];
		}
		if (platformCount.pid[i] == "3") {
			c_ln = platformCount.count[i];
		}
		if (platformCount.pid[i] == "4") {
			c_gg = platformCount.count[i];
		}
	}
	document.getElementById("fb_count").innerHTML = c_fb;
	document.getElementById("ig_count").innerHTML = c_ig;
	document.getElementById("ln_count").innerHTML = c_ln;
	document.getElementById("gg_count").innerHTML = c_gg;
}

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

// Util functions

function arrayUnion(a, b) {
	return [...new Set([...a, ...b])];
}

function removeDuplicate(arr) {
	return [...new Set([...arr])];
}

function areObjectsEqual(obj1, obj2) {
	const props1 = Object.entries(obj1);
	const props2 = Object.entries(obj2);

	if (props1.length !== props2.length) {
		return false;
	}

	for (let i = 0; i < props1.length; i++) {
		const [key1, value1] = props1[i];
		const [key2, value2] = props2[i];

		if (key1 !== key2 || value1 !== value2) {
			return false;
		}
	}

	return true;
}

function formArray(data) {
	let arr = [];
	try {
		for (const [key, value] of Object.entries(data)) {
			arr.push(value);
		}
	} catch (error) {
		console.error(error);
	}

	return arr;
}

function throwError(Error, mode) {
	if (mode) {
		Error.classList.remove("hidden");
	} else {
		Error.classList.add("hidden");
	}
}

function jsonParseQuot(jsonForm) {
	return JSON.parse(jsonForm.replace(/&quot;/g, '"'));
}

function jsonParseQuotArray(array) {
	if (array == null) {
		return [];
	}
	array = removeDuplicate(array);
	arr = [];
	for (let i = 0; i < array.length; i++) {
		arr.push(jsonParseQuot(array[i]));
	}
	return arr;
}

function capitalizeFirstLetter(string) {
	return string
		.toLowerCase()
		.split("_")
		.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
		.join(" ");
}

function createWarning(msg, target_div) {
	var target = document.getElementById(target_div);
	warning = `<div class="alert alert-warning alert-dismissible fade show" role="alert"><i class="bi bi-exclamation-triangle-fill"></i> <b>คำเตือน:</b> ${msg}  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
	target.innerHTML += warning;
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

function removeElementsByClass(className) {
	const elements = document.getElementsByClassName(className);
	while (elements.length > 0) {
		elements[0].parentNode.removeChild(elements[0]);
	}
}

function getAllInputValue(arr, format) {
	let res = [];
	arr.forEach((i) => {
		var target = format + i;
		res.push(document.getElementById(target).value);
	});
	return res;
}

// Constructing functions

function fillRatioDonut(target) {
	target_div = document.getElementById(target);
	for (let i = 0; i < multiple_selector.length; i++) {
		target_div.innerHTML += `
		<div class="col-3 d-flex">
				<div class="card">
					<div class="card-body donut-chart-card">
						<p class="graph-title">แผนภาพเปรียบเทียบผลรวม<br />${capitalizeFirstLetter(multiple_selector[i])} ของแต่ละแพลตฟอร์ม</p>
						<div class="d-flex justify-content-center align-items-center">
							<canvas id="rd-${i}"></canvas>
						</div>
					</div>
				</div>
			</div>
		`;
	}
}

function fillTopRankTable(target) {
	target_div = document.getElementById(target);
	filterered_selector = [];
	for (let i = 0; i < multiple_selector.length; i++) {
		if (["reach", "impression", "engagement"].includes(multiple_selector[i])) {
			filterered_selector.push(multiple_selector[i]);
		}
	}
	for (let i = 0; i < topCPRarray.length; i++) {
		target_div.innerHTML += `
			<div class="col">
			<div class="card">
			<div class="card-body padding-little">
				<p class="graph-title">แคมเปญ 5 อันดับสูงสุดตามค่า Cost/${capitalizeFirstLetter(filterered_selector[i])}</p>
				<table class="table cell h-100">
					<thead class="table-dark">
						<tr>
							<th scope="col">Rank</th>
							<th scope="col">Campaign</th>
							<th scope="col" id="topCPR-th-${i}"></th>
						</tr>
					</thead>
					<tbody id="tb-topCPR-${i}"></tbody>
				</table>
			</div>
		</div>
		</div>`;
		construct_table(getTopCostPerResult(topCPRarray[i], filterered_selector[i]), `tb-topCPR-${i}`, top_range, `c-${i}`);
		document.getElementById(`topCPR-th-${i}`).innerHTML = `Cost/<br />${capitalizeFirstLetter(filterered_selector[i])}`;
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

function addPeriodInput(target_id, i) {
	const target = document.getElementById(target_id);
	var inputFormat = `<div class="period-input-${i}">
			<div class="d-flex justify-content-between">
			<label for="period-${i}">พีเรียดที่ ${i}: </label>
			<div class="d-inline-flex">
				<select class="form-select" aria-label="period" id="period-filter-${i}">
					<option selected>-</option>
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="5">5</option>
					<option value="6">6</option>
					<option value="7">7</option>
					<option value="8">8</option>
					<option value="9">9</option>
					<option value="10">10</option>
					<option value="11">11</option>
					<option value="12">12</option>
					<option value="13">13</option>
				</select>
				<select class="form-select" aria-label="year" id="year-filter-${i}" onchange="throwError(E6, false)";>
					<option selected>-</option>
				</select>
			</div>
			</div>
		</div>`;
	target.insertAdjacentHTML("beforeend", inputFormat);
	fillSelect(`year-filter-${i}`, formArray(possibleYear["year"]));
}

// Trigger functions

function periodInc() {
	const i = periodArray.length + 1;
	periodArray.push(i);
	addPeriodInput("period-array", i);
	document.getElementById("period-counter").innerHTML = i;
}

function pageInc() {
	querySubmit(page + 1);
}

function pageDec() {
	querySubmit(page - 1);
}

function periodDec() {
	const i = periodArray.length - 1;
	if (i > 0) {
		periodArray.splice(i);
		removeElementsByClass(`period-input-${i + 1}`);
		document.getElementById("period-counter").innerHTML = i;
		throwError(E6, false);
	}
}

function queryClear() {
	window.location.href = `/`;
}

function querySubmit(page = 1) {
	var startdate = document.getElementById("startdate").value;
	var enddate = document.getElementById("enddate").value;
	var periods = getAllInputValue(periodArray, "period-filter-");
	var years = getAllInputValue(periodArray, "year-filter-");

	var platform = getListCheckedBox("platform-query").toString();
	if (document.querySelector('input[name="single-selector"]:checked') == null) {
		single_selector = "";
	} else {
		single_selector = document.querySelector('input[name="single-selector"]:checked').id;
	}
	var multiple_selector = getListCheckedBox("multiple-selector").toString();

	let ref = "/?";

	if (currently_interval == "date-tab") {
		ref = ref + `&by=date`;
		if (startdate != "") {
			ref = ref + `&startdate=${startdate}`;
		}
		if (enddate != "") {
			ref = ref + `&enddate=${enddate}`;
		}
	}
	if (currently_interval == "period-tab") {
		if (years.includes("-")) {
			throwError(E6, true);
			return;
		}
		if (
			periods.includes("-") &&
			periods.filter((x) => {
				return x == "-";
			}).length != periodArray.length
		) {
			throwError(E7, true);
			return;
		}

		ref = ref + `&by=period`;
		ref = ref + `&p=${page}`;
		periods = periods.toString().replace(/-/g, "");
		years = years.toString();
		ref = ref + `&periods=${periods}`;
		ref = ref + `&years=${years}`;
	}

	if (platform != "") {
		ref = ref + `&platform=${platform}`;
	}
	if (multiple_selector != "") {
		ref = ref + `&ms=${multiple_selector}`;
	}
	ref = ref.substring(0, 2) + ref.substring(3);

	// window.location.href = `/?startdate=${startdate}&enddate=${enddate}&platform=${platform}&ss=${single_selector}`;
	window.location.href = ref;
}
