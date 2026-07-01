import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddGameForm } from './add-game-form.component';

describe('AddGameForm', () => {
  let component: AddGameForm;
  let fixture: ComponentFixture<AddGameForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddGameForm],
    }).compileComponents();

    fixture = TestBed.createComponent(AddGameForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
