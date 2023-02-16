var summary = jsonParseQuot(summaryJSON);
var costPerResult = jsonParseQuot(CPRJSON);
var summaryPerMonth = jsonParseQuot(summaryPMJSON);
// var topCPO = JSON.parse(topCPOJSON.replace(/&quot;/g, '"'));
var simpleCampaign = jsonParseQuot(simpleCampaignJSON);
var platformCount = jsonParseQuot(platformCountJSON);
var topCampaign = jsonParseQuot(topCampaignJSON);

console.log(topCampaign);

console.log(platformCount);

var topCPRarray = [];
if (topCPRSTR) {
	topCPRarray = jsonParseQuotArray(topCPRSTR.split("|"));
}

console.log(topCPRarray);

platform = platform.split(",");
multiple_selector = multiple_selector.split(",");

const platform_range = Object.keys(summary.pid).length;
const platform_count_range = Object.keys(platformCount.pid).length;
const objective_range = Object.keys(costPerResult.objective).length;
const top_range = Object.keys(topCPRarray[0].cid).length;

construct_table(summary, "db1", platform_range, "a");
construct_table(costPerResult, "db2", objective_range, "b");

function initParams() {
	document.getElementById("startdate").value = startdate;
	document.getElementById("enddate").value = enddate;
	fillCheckboxPlatform("platform-query", platform);
	fillCheckbox("multiple-selector", multiple_selector);

	fillCount();
	fillTopRankTable("top-rank-CPR");

	// document.getElementById("topCPO-th").innerHTML = `Cost/<br>${capitalizeFirstLetter(single_selector)}`;
}
initParams();

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

function jsonParseQuot(jsonForm) {
	return JSON.parse(jsonForm.replace(/&quot;/g, '"'));
}

function jsonParseQuotArray(array) {
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

fillRatioDonut("chart-test-1");

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
	if (multiple_selector != "") {
		ref = ref + `&ms=${multiple_selector}`;
	}
	ref = ref.substring(0, 2) + ref.substring(3);

	// window.location.href = `/?startdate=${startdate}&enddate=${enddate}&platform=${platform}&ss=${single_selector}`;
	window.location.href = ref;
}
