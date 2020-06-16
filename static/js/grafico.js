function lineChart(x) {
  console.log(x);
  var w = JSON.parse(x);
  window.lineChart = Morris.Line({
    element: 'line-chart',

    data: w,
    xkey: 'y',
    // ykeys: ['a', 'b'],
    ykeys: ['v'],

    // labels: ['Series A', 'Series B'],
    labels: ['Avistamientos'],

    // lineColors: ['#1e88e5','#ff3321'],
    lineColors: ['#ff99c6'],
    lineWidth: '3px',
    pointFillColors: ['#4B0082'],
    resize: true,
    redraw: true
  });
}