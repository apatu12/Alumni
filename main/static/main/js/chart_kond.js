fetch('{{ url_for('api/kondisi') }}')
            .then(response => response.json())
            .then(data => {
                Highcharts.chart('container', {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: ''
                    },
                    xAxis: {
                        categories: data.categories
                    },
                    yAxis: {
                        title: {
                            text: 'Total Tranzaksaun'
                        }
                    },
                    series: data.series
                });
            })
            .catch(error => console.error('Error fetching data:', error));