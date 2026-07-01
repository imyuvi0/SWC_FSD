import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, AbstractControl, ValidationErrors } from '@angular/forms';
import { GameService } from '../../services/game.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-add-game-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './add-game-form.component.html',
  styleUrls: ['./add-game-form.component.css']
})
export class AddGameFormComponent implements OnInit {
  gameForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private gameService: GameService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  initForm(): void {
    this.gameForm = this.fb.group({
      // title control: initial value empty string, validators: required, and custom uppercase check
      title: ['', [Validators.required, this.titleUppercaseValidator]],
      // price control: initial value 0, validators: required and minimum value 1
      price: [0, [Validators.required, Validators.min(1)]]
    });
  }

  // Custom Validator: Checks if the first letter of the game title is capitalized
  // Returns null if valid, or a ValidationErrors object if invalid
  titleUppercaseValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value as string;
    if (!value) return null; // Let 'required' validator handle empty values
    
    const firstLetter = value.charAt(0);
    if (firstLetter !== firstLetter.toUpperCase()) {
      return { 'titleUppercase': true };
    }
    return null;
  }

  onSubmit(): void {
    if (this.gameForm.invalid) {
      this.gameForm.markAllAsTouched();
      return;
    }
    const { title, price } = this.gameForm.value;
    this.gameService.addGame(title, price).subscribe({
      next: () => {
        this.router.navigate(['/games']);
      },
      error: (err) => {
        console.error('Error adding game via form: ', err);
      }
    });
  }
}
