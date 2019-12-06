import { Component, OnInit } from '@angular/core';
import {AuthService} from '../authentication/authService';

@Component({
  selector: 'app-patient-overview',
  templateUrl: './patient-overview.component.html',
  styleUrls: ['./patient-overview.component.css']
})
export class PatientOverviewComponent implements OnInit {

    patients = [];


  constructor(private authService: AuthService) { }

  ngOnInit() {
      let i = 0;
      let test =this.authService.getPatients()
          .subscribe((value) => {
              console.log(value);
              for (let patient in value)
              {
                  this.patients.push(value[i])
                   i++
              }
          });

  }


}
