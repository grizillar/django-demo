const PERIODINYEAR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

var earliestMonth;
var lastestMonth;

function monthof(index) {
	const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
	return monthNames[index - 1];
}

function formDateRange() {
	var monthLength = Object.keys(summaryPerMonth.month).length;
	earliestMonth = [summaryPerMonth.month[0], summaryPerMonth.year[0]];
	lastestMonth = [summaryPerMonth.month[monthLength - 1], summaryPerMonth.year[monthLength - 1]];

	var currmonth = earliestMonth[0];
	var curryear = earliestMonth[1];

	var month = [];
	var year = [];

	while (curryear <= lastestMonth[1]) {
		month.push(currmonth);
		year.push(curryear);

		if (currmonth == lastestMonth[0] && curryear == lastestMonth[1]) {
			break;
		}

		currmonth++;
		if (currmonth > 12) {
			currmonth = 1;
			curryear++;
		}
	}

	return [month, year];
}

function formPeriodRange(period, year) {
	const period_start = parseInt(period[0]);
	const period_end = parseInt(period[1]);
	const year_start = parseInt(year[0]);
	const year_end = parseInt(year[1]);

	const isPeriodSame = period_start == period_end;
	const isYearSame = year_start == year_end;

	if (isYearSame) {
		if (isPeriodSame) {
			return {
				periods: [period_start],
				years: [year_start],
			};
		} else {
			var periods = [];
			var years = [];
			for (let i = period_start; i <= period_end; i++) {
				periods.push(i);
				years.push(year_start);
			}
			return {
				periods: periods,
				years: years,
			};
		}
	} else {
		var periods = [];
		var years = [];
		let currperiod = period_start;
		let curryear = year_start;
		while (curryear < year_end) {
			periods.push(currperiod);
			years.push(curryear);
			if (currperiod >= 13) {
				curryear++;
				currperiod = 1;
			} else {
				currperiod++;
			}
		}
		for (let i = 1; i <= period_end; i++) {
			periods.push(i);
			years.push(curryear);
		}
		return {
			periods: periods,
			years: years,
		};
	}
}

function fillTitleNameSPMT(target_p, earliestMonth, lastestMonth) {
	var target = document.getElementById(target_p);
	target.innerHTML += `ตั้งแต่ ${monthof(earliestMonth[0])}, ${earliestMonth[1]} ถึง ${monthof(lastestMonth[0])}, ${lastestMonth[1]}`;
}

function interpretDate(range) {
	var dateArr = [];
	for (let i = 0; i < range[0].length; i++) {
		dateArr.push(`${monthof(range[0][i])}, ${range[1][i]}`);
	}
	return dateArr;
}

function interpretPeriod(range) {
	var periodArr = [];
	for (let i = 0; i < range.length; i++) {
		periodArr.push(`พีเรียด ${range[i]}`);
	}
	return periodArr;
}

function fillDataByDate(sumdata, data, range) {
	const monthArr = formArray(sumdata.month);
	const yearArr = formArray(sumdata.year);
	const dataArr = formArray(data);

	if (dataArr.length == 0) {
		return dataArr;
	}

	var filledArr = [];
	let currDate = 0;

	for (let i = 0; i < range[0].length; i++) {
		if (range[0][i] == monthArr[currDate] && range[1][i] == yearArr[currDate]) {
			filledArr.push(dataArr[currDate]);
			currDate++;
		} else {
			filledArr.push(0);
		}
	}

	return filledArr;
}

function fillDataByPeriod(sumdata, data) {
	const dataArr = formArray(data);

	var filledArr = [];
	let currPeriod = 1;
	for (let i = 0; i < 13; i++) {
		if (formArray(sumdata.period).includes(PERIODINYEAR[i])) {
			filledArr.push(dataArr[currPeriod - 1]);
			currPeriod++;
		} else {
			filledArr.push(0);
		}
	}
	return filledArr;
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

function formDatasetWithDate(data, target_list) {
	// var labels = [];
	// for (let i = 0; i < target_list.length; i++) {
	// 	if (["spending", "reach", "impression", "engagement"].includes(target_list[i])) {
	// 		labels.push(target_list[i]);
	// 	}
	// }
	var labels = target_list;
	var datasets = [];
	for (let i = 0; i < labels.length; i++) {
		var label = {
			label: capitalizeFirstLetter(labels[i]),
			data: fillDataByDate(data, data[labels[i]], formDateRange()),
		};
		datasets.push(label);
	}
	return datasets;
}

// Can choose only one
function formDatasetWithPeriod(target) {
	var labels = removeDuplicate(year);
	if (compare) {
		labels = removeDuplicate(year.concat(year_2));
	}
	var datasets = [];
	for (let i = 0; i < labels.length; i++) {
		var label = {
			label: labels[i],
			data: fillDataByPeriod(summaryByPeriodArray[i], summaryByPeriodArray[i][target]),
		};
		datasets.push(label);
	}
	return datasets;
}

function formScatterData(data, target_x, target_y) {
	var arr = [];
	var x_arr = formArray(data[target_x]);
	var y_arr = formArray(data[target_y]);
	var name_arr = formArray(data["name"]);
	for (let i = 0; i < x_arr.length; i++) {
		//LIMIT
		if (x_arr[i] < LIMIT.count && y_arr[i] < LIMIT.spending) {
			let obj = {};
			obj["x"] = x_arr[i];
			obj["y"] = y_arr[i];
			obj["name"] = name_arr[i];
			if (x_arr[i] != 0) {
				arr.push(obj);
			}
		}
	}
	return arr;
}

function formScatterDataset(data, target_list) {
	var datasets = [];
	for (let i = 0; i < target_list.length; i++) {
		if (["reach", "impression", "engagement"].includes(target_list[i])) {
			var obj = {
				label: capitalizeFirstLetter(target_list[i]),
				data: formScatterData(data, target_list[i], "spending"),
			};
			datasets.push(obj);
		}
	}
	return datasets;
}

function capitalizeFirstLetter(string) {
	return string
		.toLowerCase()
		.split("_")
		.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
		.join(" ");
}

function formRatioDonutData(label) {
	return {
		labels: formArray(summary.platform_name),
		datasets: [
			{
				data: formArray(summary[label]),
				// backgroundColor: ["rgb(255, 51, 51)", "rgb(255, 255, 102)", "rgb(255, 205, 86)"],
				hoverOffset: 10,
			},
		],
	};
}

function formRatioDonutDatasets(target_list) {
	datasets = [];
	for (let i = 0; i < target_list.length; i++) {
		datasets.push({
			label: target_list[i],
			data: formArray(summary[target_list[i]]),
			backgroundColor: filteredPlatformColor,
			hoverOffset: 4,
		});
	}
	return datasets;
}

function filteredPlatformColor() {
	const color_range = ["rgb(66,103,178)", "rgb(255, 51, 153)", "rgb(102, 255, 102)", "rgb(255, 80, 80)", "rgb(255, 255, 102)", "rgb(204, 0, 153)", "rgb(204, 204, 204)"];
	var color = [];
	platform.forEach((p) => {
		color.push(color_range[parseInt(p) - 1]);
	});
	return color;
}

function filteredPlatformColorByPlatformName(platform_name) {
	var color = [];
	if (platform_name.includes("Facebook")) {
		color.push("rgb(66,103,178)");
	}
	if (platform_name.includes("Instagram")) {
		color.push("rgb(255, 51, 153)");
	}
	if (platform_name.includes("Line")) {
		color.push("rgb(102, 255, 102)");
	}
	if (platform_name.includes("Google Ads")) {
		color.push("rgb(255, 80, 80)");
	}
	if (platform_name.includes("Google Organic")) {
		color.push("rgb(255, 255, 102)");
	}
	if (platform_name.includes("Website")) {
		color.push("rgb(204, 0, 153)");
	}
	if (platform_name.includes("Other")) {
		color.push("rgb(204, 204, 204)");
	}
	return color;
}

function getPeriodRangeName() {
	var time_text = "";
	var range_text = "";
	var time_text_2 = "";
	var range_text_2 = "";
	var isYearSame = year[0] == year[1];
	var isPeriodSame = period[0] == period[1];
	if (isYearSame) {
		if (isPeriodSame) {
			time_text = `พีเรียดที่ ${period[0]}, ปี ${year[0]}`;
			range_text = `${period[0]}, ${year[0]}`;
		} else {
			time_text = `ตั้งแต่พีเรียดที่ ${period[0]} ถึงพีเรียดที่ ${period[1]}, ปี ${year[0]}`;
			range_text = `${period[0]} - ${period[1]}, ${year[0]}`;
		}
	} else {
		time_text = `ตั้งแต่พีเรียดที่ ${period[0]}, ปี ${year[0]} ถึงพีเรียดที่ ${period[1]}, ปี ${year[1]}`;
		range_text = `${period[0]}, ${year[0]} - ${period[1]}, ${year[1]}`;
	}

	if (compare) {
		var isYearSame_2 = year_2[0] == year_2[1];
		var isPeriodSame_2 = period_2[0] == period_2[1];
		if (isYearSame_2) {
			if (isPeriodSame_2) {
				time_text_2 = `พีเรียดที่ ${period_2[0]}, ปี ${year_2[0]}`;
				range_text_2 = `${period_2[0]}, ${year_2[0]}`;
			} else {
				time_text_2 = `ตั้งแต่พีเรียดที่ ${period_2[0]} ถึงพีเรียดที่ ${period_2[1]}, ปี ${year_2[0]}`;
				range_text_2 = `${period_2[0]} - ${period_2[1]}, ${year_2[0]}`;
			}
		} else {
			time_text_2 = `ตั้งแต่พีเรียดที่ ${period_2[0]}, ปี ${year_2[0]} ถึงพีเรียดที่ ${period_2[1]}, ปี ${year_2[1]}`;
			range_text_2 = `${period_2[0]}, ${year_2[0]} - ${period_2[1]}, ${year_2[1]}`;
		}
	}
	return {
		period_1st: {
			text: time_text,
			range: range_text,
		},
		period_2nd: {
			text: time_text_2,
			range: range_text_2,
		},
	};
}

function fillDountExecute() {
	const color_range = ["rgb(66,103,178)", "rgb(255, 51, 153)", "rgb(102, 255, 102)", "rgb(255, 80, 80)", "rgb(255, 255, 102)", "rgb(204, 0, 153)", "rgb(204, 204, 204)"];

	function filteredNullandZero(arr, arr_platform_name) {
		var new_arr = [];
		var new_platform = [];
		for (let i = 0; i < arr.length; i++) {
			if (arr[i] != 0 && arr[i] != null) {
				new_arr.push(arr[i]);
				new_platform.push(arr_platform_name[i]);
			}
		}
		return {
			data: new_arr,
			platform: new_platform,
		};
	}

	for (let i = 0; i < multiple_selector.length; i++) {
		var filtered_data = filteredNullandZero(formArray(summary[multiple_selector[i]]), formArray(summary.platform_name));
		var data_d = {
			labels: filtered_data.platform,
			datasets: [
				{
					label: multiple_selector[i],
					data: filtered_data.data,
					backgroundColor: filteredPlatformColorByPlatformName(filtered_data.platform),
					hoverOffset: 4,
				},
			],
		};

		if (by == "period") {
			if (compare) {
				var filtered_data_2 = filteredNullandZero(formArray(summary_2[multiple_selector[i]]), formArray(summary_2.platform_name));
				data_d.datasets.push({
					label: multiple_selector[i],
					data: filtered_data_2.data,
					backgroundColor: filteredPlatformColorByPlatformName(filtered_data_2.platform),
					hoverOffset: 4,
				});
				var platform_label = arrayUnion(filtered_data.platform, filtered_data_2.platform);
				data_d.labels = platform_label;
			}
		}

		var config_d = {
			type: "doughnut",
			data: data_d,
			options: {
				respondsive: true,
				plugins: {
					tooltip: {
						callbacks: {
							title: (context) => {
								var index = context[0].datasetIndex;
								if (by == "date") {
									return context.title;
								}
								if (by == "period") {
									if (!compare) {
										return getPeriodRangeName().period_1st.range;
									} else {
										if (index == 0) {
											return getPeriodRangeName().period_1st.range;
										}
										if (index == 1) {
											return getPeriodRangeName().period_2nd.range;
										}
									}
								}
								// if (period[index] == "") {
								// 	return `ปี ${year[index]}`;
								// }
								// return `พีเรียด ${period[index]}, ปี ${year[index]}`;
							},
							label: (context) => {
								let label = context.label;
								let value = parseInt(context.parsed);

								if (!label) label = "Unknown";

								let dataArr = context.chart.data.datasets[context.datasetIndex].data;

								const total = dataArr.reduce((total, dataArr) => total + dataArr, 0);
								const percentage = Math.round((value / total) * 100);

								return label + ": " + percentage + "%";
							},
						},
					},
					title: {
						display: false,
						text: `${capitalizeFirstLetter("reach")} Count`,
					},
					datalabels: {
						display: false,
						formatter: (value, ctx) => {
							const datapoints = ctx.chart.data.datasets[0].data;
							const total = datapoints.reduce((total, datapoint) => total + datapoint, 0);
							const percentage = (value / total) * 100;
							return percentage.toFixed(2) + "%";
						},
						color: "#000000",
					},
				},
			},
			plugins: [ChartDataLabels],
		};
		new Chart(document.getElementById(`rd-${i}`), config_d);
	}
}

function fillCompareBarGraphExecute() {
	if (by == "period" && compare) {
		for (let i = 0; i < multiple_selector.length; i++) {
			const period_range = getPeriodRangeName();
			const labels = [period_range.period_1st.range, period_range.period_2nd.range];
			const data = {
				labels: labels,
				datasets: [
					{
						label: multiple_selector[i],
						data: [totalSummary[multiple_selector[i]][0], totalSummary_2[multiple_selector[i]][0]],
						borderWidth: 1,
					},
				],
			};
			const config = {
				type: "bar",
				data: data,
				options: {
					scales: {
						y: {
							beginAtZero: true,
						},
					},
					barPercentage: 0.8,
				},
			};
			new Chart(document.getElementById(`cbg-${i}`), config);
		}
	}
}

const data_d1 = {
	labels: formArray(summary.platform_name),
	datasets: formRatioDonutDatasets(multiple_selector),
};

// const data_s1 = {
// 	datasets: formScatterDataset(simpleCampaign, multiple_selector),
// };

// const data_sb1 = {
// 	labels: formArray(topCampaign.name),
// 	datasets: [
// 		{
// 			label: "Reach",
// 			data: formArray(topCampaign.reach),
// 		},
// 		{
// 			label: "Impression",
// 			data: formArray(topCampaign.impression),
// 		},
// 		{
// 			label: "Engagement",
// 			data: formArray(topCampaign.engagement),
// 		},
// 	],
// };

const config_d1 = {
	type: "doughnut",
	data: data_d1,
	options: {
		respondsive: true,
		plugins: {
			title: {
				display: false,
				text: `${capitalizeFirstLetter("reach")} Count`,
			},
		},
	},
};

fillDountExecute();
fillCompareBarGraphExecute();
var currChart = createPeriodLineGraph();

function createPeriodLineGraph(target = "engagement") {
	if (by == "date") {
		const data_l1_d = {
			labels: interpretDate(formDateRange()),
			datasets: formDatasetWithDate(summaryPerMonth, [target]),
		};

		const config_l1_d = {
			type: "line",
			data: data_l1_d,
			options: {
				responsive: true,
				plugins: {
					legend: {
						position: "top",
					},
					title: {
						display: false,
						text: "Summation per Month",
					},
				},
			},
		};
		document.getElementById("summary-per-title").innerHTML = `กราฟผลรวมต่อเดือนตั้งแต่ ${monthof(earliestMonth[0])}, ${earliestMonth[1]} ถึง ${monthof(lastestMonth[0])}, ${lastestMonth[1]}`;
		// fillTitleNameSPMT("summary-per-month-title", earliestMonth, lastestMonth);
		return new Chart(document.getElementById("line-1"), config_l1_d);
	}

	if (by == "period") {
		const data_l1_p = {
			labels: interpretPeriod(PERIODINYEAR),
			datasets: formDatasetWithPeriod(target),
		};

		const config_l1_p = {
			type: "line",
			data: data_l1_p,
			options: {
				responsive: true,
				plugins: {
					legend: {
						position: "top",
					},
					title: {
						display: false,
						text: "Summation per Month",
					},
				},
			},
		};
		var allyear = removeDuplicate(year);
		if (compare) {
			allyear = removeDuplicate(year.concat(year_2));
		}
		document.getElementById("summary-per-title").innerHTML = `กราฟผลรวมทั้งปี ${allyear.toString()} แบ่งตามพีเรียด`;
		return new Chart(document.getElementById("line-1"), config_l1_p);
	}
}

// detectEmptyLabel(config_l1, "g-l1");

function minorDropdown(target) {
	currChart.destroy();
	currChart = createPeriodLineGraph(target);
}

function detectEmptyLabel(config, target_div) {
	var datasets = config.data.datasets;
	for (let i = 0; i < datasets.length; i++) {
		if (datasets[i].data.length == 0) {
			var message = `ไม่พบเวลาที่สัมพันธ์กับข้อมูล ${datasets[i].label}`;
			createWarning(message, target_div);
		}
	}
}
