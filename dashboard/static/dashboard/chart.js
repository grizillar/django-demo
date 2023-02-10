function monthof(index) {
	const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
	return monthNames[index - 1];
}

function formDateRange() {
	var monthLength = Object.keys(summaryPerMonth.month).length;
	var earliestMonth = [summaryPerMonth.month[0], summaryPerMonth.year[0]];
	var lastestMonth = [summaryPerMonth.month[monthLength - 1], summaryPerMonth.year[monthLength - 1]];

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

function formDatasetWithDate(data, labels) {
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

function capitalizeFirstLetter(string) {
	return string
		.toLowerCase()
		.split("_")
		.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
		.join(" ");
}

const data_d1 = {
	labels: formArray(summary.platform_name),
	datasets: [
		{
			label: "Label here",
			data: formArray(summary[single_selector]),
			// backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"],
			hoverOffset: 4,
		},
	],
};

// const data_l1 = {
// 	labels: interpretDate(formDateRange()),
// 	datasets: [
// 		{
// 			label: "Reach",
// 			data: fillDataByDate(summaryPerMonth, summaryPerMonth.reach, formDateRange()),
// 			// borderColor: Utils.CHART_COLORS.red,
// 			// backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
// 		},
// 		{
// 			label: "Impression",
// 			data: fillDataByDate(summaryPerMonth, summaryPerMonth.impression, formDateRange()),
// 		},
// 		{
// 			label: "Engagement",
// 			data: fillDataByDate(summaryPerMonth, summaryPerMonth.engagement, formDateRange()),
// 		},
// 	],
// };

const data_l1 = {
	labels: interpretDate(formDateRange()),
	datasets: formDatasetWithDate(summaryPerMonth, multiple_selector),
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
				display: true,
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
				display: true,
				text: `${capitalizeFirstLetter(single_selector)} Count`,
			},
		},
	},
};

// Always before draw Chart
detectEmptyLabel(config_l1, "g-l1");

new Chart(document.getElementById("donut-1"), config_d1);

new Chart(document.getElementById("line-1"), config_l1);

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
