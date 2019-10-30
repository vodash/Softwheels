import {Component, OnInit} from '@angular/core';
import * as Highcharts from 'highcharts';
import {AuthService} from '../authentication/authService';

@Component({
   selector: 'app-chart',
   templateUrl: './chart.component.html',
   styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {
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
      series: [{
         name: 'Tokyo',
         data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2]
      },
      {
         name: 'New York',
         data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8]
      },
      {
         name: 'Berlin',
         data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6]
      },
      {
         name: 'London',
         data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0]
      }]
   };
   constructor(private authService: AuthService
    ) {}
    ngOnInit() {
        this.authService.GetdataonID()
            .subscribe(
                () => {
                }
            );
    }
    setdata() {

    }
}
