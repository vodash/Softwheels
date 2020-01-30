import { Component, OnInit } from '@angular/core';
import {AuthService} from '../../authentication/authService';

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.css']
})
export class PatientListComponent implements OnInit {

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
