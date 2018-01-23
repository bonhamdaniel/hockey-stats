var strX = "999.99;-89.01;-60.29;-145.83;-140.76;-148.24;-88.70;56.92;69.08;-121.37";
var strY = "143.12;146.51;143.73;177.58;121.68;116.45;-14.05;20.77;15.82;168.20";
var colorCode = "CPPEEECTTE", colorArr = [];
for(var i = 0; i < colorCode.length; i++) {
  if(colorCode[i] === "C")
    colorArr.push("blue");
  else if(colorCode[i] === "P")
    colorArr.push("green");
  else if(colorCode[i] === "E")
    colorArr.push("yellow");
  else
    colorArr.push("red");
}

var chart = new CanvasJS.Chart("locationmap", {
  title:{
    text: "Title of my scatter chart"
  },

  data: [
    {
      type: "scatter",
      dataPoints: []
    }
  ]
});
var xVal = strX.split(";");
var yVal = strY.split(";");

for(var i = 0; i < xVal.length; i++) {
  chart.options.data[0].dataPoints.push({
    x: parseFloat(xVal[i]),
    y: parseFloat(yVal[i]),
    color: colorArr[i]
  });
}

chart.render();