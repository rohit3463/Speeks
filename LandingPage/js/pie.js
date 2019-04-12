google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Emotion', 'value per Frame'],
          ['Anger',     11],
          ['Disgust',      2],
          ['Fear',  4],
          ['Sad', 8],
          ['Surprise',    7],
          ['Neutral', 10]
        ]);

        var options = {
          title: 'Face Emotion'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }