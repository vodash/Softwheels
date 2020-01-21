import {Component, OnInit} from '@angular/core';
import * as Highcharts from 'highcharts/highstock';
import {AuthService} from '../authentication/authService';
import {ChartData} from '../models/chartdata.model';
// import * as $ from 'jquery';

declare var $timeout: any
@Component({
   selector: 'app-chart',
   templateUrl: './chart.component.html',
   styleUrls: ['./chart.component.css']
})

export class ChartComponent implements OnInit {
    Chartdata: ChartData[];
    xaxis = [];

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
            valueSuffix: ''
            }
        ,
	// function (chart) {
    //         // apply the date pickers
    //         $timeout(function () {
    //             (<any>$('input.highcharts-input-group')).datepicker();
    //         }, 0);
    //     },
        series: [
            {
                name: 'Activity',
                data: []
            },
            {
                name: 'Sleep',
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
        this.authService.getDataOnID().subscribe((data => {
            this.Chartdata = data;
            console.log(this.Chartdata['hoi'][0]['data']);
            let charter = Highcharts.stockChart('container2', this.options);
            charter.series[0].setData(this.Chartdata['hoi'][0]['data']);
            charter.series[1].setData(this.Chartdata['hoi'][1]['data']);
        }));
    }
    // TODO: update this function to work with the new way we want to show it (with dates)
    xAxisData(steps) {
        console.log('clicked');
        if (steps === 'W') {
            this.xaxis = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
            console.log('hier');
        }
    }
}
