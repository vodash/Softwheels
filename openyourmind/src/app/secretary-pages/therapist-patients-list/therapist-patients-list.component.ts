import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../authentication/authService";

@Component({
  selector: 'app-therapist-patients-list',
  templateUrl: './therapist-patients-list.component.html',
  styleUrls: ['./therapist-patients-list.component.css']
})
export class TherapistPatientsListComponent implements OnInit {

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
