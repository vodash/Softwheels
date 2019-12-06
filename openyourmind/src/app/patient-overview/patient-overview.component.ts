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
      this.authService.getPatients()
          .subscribe((value) => {
              for (const patients in value) {
                  this.patients.push(value[i][1]);
                  i++;
              }
           });

  }


}
