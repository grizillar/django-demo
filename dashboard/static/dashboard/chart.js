LIMIT = {
	spending: 30000,
	count: 400000,
};

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
	var labels = ["reach", "impression", "engagement"];
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

function fillDount() {
	for (let i = 0; i < multiple_selector.length; i++) {
		var data_d = {
			labels: formArray(summary.platform_name),
			datasets: [
				{
					label: multiple_selector[i],
					data: formArray(summary[multiple_selector[i]]),
					backgroundColor: filteredPlatformColor,
					hoverOffset: 4,
				},
			],
		};
		var config_d = {
			type: "doughnut",
			data: data_d,
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
		new Chart(document.getElementById(`rd-${i}`), config_d);
	}
}

const data_d1 = {
	labels: formArray(summary.platform_name),
	datasets: formRatioDonutDatasets(multiple_selector),
};

const data_l1 = {
	labels: interpretDate(formDateRange()),
	datasets: formDatasetWithDate(summaryPerMonth, multiple_selector),
};

const data_s1 = {
	datasets: formScatterDataset(simpleCampaign, multiple_selector),
};

const data_sb1 = {
	labels: formArray(topCampaign.name),
	datasets: [
		{
			label: "Reach",
			data: formArray(topCampaign.reach),
		},
		{
			label: "Impression",
			data: formArray(topCampaign.impression),
		},
		{
			label: "Engagement",
			data: formArray(topCampaign.engagement),
		},
	],
};

const config_l1 = {
	type: "line",
	data: data_l1,
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

const config_l1_test = {
	type: "bar",
	data: data_l1,
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

const config_s1 = {
	type: "scatter",
	data: data_s1,
	options: {
		animation: {
			duration: 0,
		},
		scales: {
			x: {
				type: "linear",
				position: "bottom",
			},
		},
		plugins: {
			tooltip: {
				callbacks: {
					label: function (context) {
						return `${context.raw.name}`;
					},
				},
			},
			title: {
				display: false,
				text: `Cost Effective Scatterplot`,
			},
		},
	},
};

const config_sb1 = {
	type: "bar",
	data: data_sb1,
	options: {
		plugins: {
			title: {
				display: false,
				text: "",
			},
		},
		responsive: true,
		scales: {
			x: {
				stacked: true,
			},
			y: {
				stacked: true,
			},
		},
		indexAxis: "y",
	},
};

// Always before draw Chart
detectEmptyLabel(config_l1, "g-l1");

new Chart(document.getElementById("donut-1"), config_d1);

new Chart(document.getElementById("line-1"), config_l1);

new Chart(document.getElementById("scatter-1"), config_s1);

new Chart(document.getElementById("line-1-test"), config_l1_test);

new Chart(document.getElementById("stackbar-1"), config_sb1);

fillDount();

fillTitleNameSPMT("summary-per-month-title", earliestMonth, lastestMonth);
fillTitleNameSPMT("summary-per-month-title-bar", earliestMonth, lastestMonth);
// detectEmptyLabel(config_l1, "g-l1");

function detectEmptyLabel(config, target_div) {
	var datasets = config.data.datasets;
	for (let i = 0; i < datasets.length; i++) {
		if (datasets[i].data.length == 0) {
			var message = `ไม่พบเวลาที่สัมพันธ์กับข้อมูล ${datasets[i].label}`;
			createWarning(message, target_div);
		}
	}
}
