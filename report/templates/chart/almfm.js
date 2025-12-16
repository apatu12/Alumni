$.get("/api/report/fun/sexo/", function(data) {

    // Hitung total (mane + feto)
    const total = data.obj_mane.map((m, i) => m + data.obj_feto[i]);

    Highcharts.chart('chartCombo', {
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: 'Distribuição de Alumni por Sexo e Faculdade'
        },

        xAxis: [{
            categories: data.label,
            crosshair: true,
            labels: {
                rotation: -45
            }
        }],

        yAxis: [{  // Y-Axis kiri (untuk column)
            title: {
                text: 'Total por Sexo'
            },
            min: 0
        }, {  // Y-Axis kanan (untuk line total)
            title: {
                text: 'Total Geral'
            },
            opposite: true
        }],

        tooltip: {
            shared: true,
            headerFormat: '<b>{point.key}</b><br/>'
        },

        plotOptions: {
            column: {
                pointPadding: 0.1,
                borderWidth: 0
            }
        },

        series: [
            {
                name: 'Masculino',
                type: 'column',
                data: data.obj_mane,
                color: '#3498db'
            },
            {
                name: 'Femenino',
                type: 'column',
                data: data.obj_feto,
                color: '#e74c3c'
            },
            {
                name: 'Total',
                type: 'line',
                yAxis: 1,
                data: total,
                color: '#2ecc71',
                lineWidth: 3,
                marker: {
                    enabled: true,
                    radius: 5
                }
            }
        ]
    });

});
