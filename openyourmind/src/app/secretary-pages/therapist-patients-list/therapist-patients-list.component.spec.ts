import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TherapistPatientsListComponent } from './therapist-patients-list.component';

describe('TherapistPatientsListComponent', () => {
  let component: TherapistPatientsListComponent;
  let fixture: ComponentFixture<TherapistPatientsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TherapistPatientsListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TherapistPatientsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
