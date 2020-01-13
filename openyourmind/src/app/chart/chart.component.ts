import {Component, OnInit} from '@angular/core';
import * as Highcharts from 'highcharts/highstock';
import {AuthService} from '../authentication/authService';
import {ChartData} from '../models/chartdata.model';

@Component({
   selector: 'app-chart',
   templateUrl: './chart.component.html',
   styleUrls: ['./chart.component.css']
})

export class ChartComponent implements OnInit {
    Chartdata: ChartData[];

    public options: any = {
        chart: {
            type: 'spline',
            height: 700,
            backgroundColor: 'none'
        },
        // title: {
        //     text: 'Test'
        // },
        legend: {
			enabled: true,
            align: 'center',
            verticalAlign: 'top',
            layout: 'horizontal',
            // x: 0,
            // y: 0,
            // symbolWidth: 0,
            // itemMarginBottom: 60,
            // itemMarginTop: 0,
            itemStyle: {
                color: '#333333',
                cursor: 'pointer',
                fontSize: '20px',
                fontWeight: 'bold',
            }
        },
        credits: {
            enabled: false
        },
        tooltip: {
            valueSuffix: ' °C'
            }
        ,
        series: [
            {
                name: 'appel',
                data: []
            },
            {
                name: 'peer',
                data: []
            }
        ]}

	// 	$.datepicker.setDefaults({
    //     dateFormat: 'dd-mm-yy',
    //     onSelect: function (dateText) {
    //         this.onchange();
    //         this.onblur();
    //     }
    // });
    constructor(private authService: AuthService
    ) {

    }

    ngOnInit() {
        this.authService.GetdataonID().subscribe((data => {
            this.Chartdata = data;
            console.log(this.Chartdata['hoi'][0]['data']);
            let charter = Highcharts.stockChart('container2', this.options);
            charter.series[0].setData(this.Chartdata['hoi'][0]['data']);
            charter.series[1].setData(this.Chartdata['hoi'][1]['data']);
        }));
    }
}
