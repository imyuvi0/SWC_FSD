import { Component, OnInit } from '@angular/core';
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
  game: Game | undefined;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService
  ) {}

  ngOnInit(): void {
    // Read the dynamic 'id' parameter from the route parameter snapshot
    const gameId = Number(this.route.snapshot.paramMap.get('id'));
    
    this.gameService.getGameById(gameId).subscribe({
      next: (game) => {
        this.game = game;
      },
      error: (err) => {
        console.error('Error fetching game details: ', err);
      }
    });
  }
}
