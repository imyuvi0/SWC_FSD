import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { GameService, Game } from '../../services/game.service';

@Component({
  selector: 'app-game-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './game-detail.component.html',
  styleUrls: ['./game-detail.component.css']
})
export class GameDetailComponent implements OnInit {
  // Use Angular Signals for reactive detail state tracking in zoneless mode
  game = signal<Game | undefined>(undefined);

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService
  ) {}

  ngOnInit(): void {
    // Read the dynamic 'id' parameter from the route parameter snapshot
    const gameId = Number(this.route.snapshot.paramMap.get('id'));
    
    this.gameService.getGameById(gameId).subscribe({
      next: (game) => {
        this.game.set(game);
      },
      error: (err) => {
        console.error('Error fetching game details: ', err);
      }
    });
  }
}
