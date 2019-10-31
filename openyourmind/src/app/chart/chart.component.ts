import {Component, OnInit} from '@angular/core';
import * as Highcharts from 'highcharts';
import {AuthService} from '../authentication/authService';
import {ChartData} from "../models/chartdata.model";

@Component({
   selector: 'app-chart',
   templateUrl: './chart.component.html',
   styleUrls: ['./chart.component.css']
})

export class ChartComponent implements OnInit {
    Chartdata: ChartData[];

    highcharts = Highcharts;
    chartOptions = {
        chart: {
            type: 'spline',
            backgroundColor: 'none'
        },
        legend: {
            align: 'center',
            verticalAlign: 'top',
            layout: 'horizontal',
            x: 0,
            y: 0,
            symbolWidth: 0,
            itemMarginBottom: 60,
            itemMarginTop: 0,
            itemStyle: {
                color: '#333333',
                cursor: 'pointer',
                fontSize: '20px',
                fontWeight: 'bold',
            }
        },
        credits: false,
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: ['M', 'T', 'W', 'T', 'F', 'S',
                'S']
        },
        yAxis: {
            title: {
                text: 'Temperature °C'
            }
        },
        tooltip: {
            valueSuffix: ' °C'
        },
        series: [
            {
                name: 'appel',
                data: []
                // this.Chartdata[0]
            },
            {
                name: 'peer',
                data: []
            }]
    };
    constructor(private authService: AuthService
    ) {

    }

    ngOnInit() {
        this.authService.GetdataonID().subscribe((data => {
            this.Chartdata = data;
            console.log(this.Chartdata['series'][0]['data']);
        }));
    }
}
