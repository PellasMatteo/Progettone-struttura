import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';
import { FoodData } from 'src/models/foodData.model';

@Injectable({
  providedIn: 'root'
})
export class AnimalsService {

  constructor(private http: HttpClient) { }

  //Il metodo fa una chiamata Http al server
  getAnimals() {
    return this.http.get<VettAnimal>('/api/animals');
  }
  httpOptions = {headers: new HttpHeaders({ 'Content-Type': 'application/json' })};
  
sendNewAnimal(animal : Animal) : Observable<Animal>
{
  return this.http.post<Animal>('/api/newAnimal', animal, this.httpOptions)
}
nutri(animal : Animal) : Observable<FoodData>
  {
    return this.http.post<FoodData>( '/api/feedAnimal', animal,this.httpOptions)
  }
}

/*
Definisco il tipo di dato che mi aspetto di ricevere dal server 
"animals": [
  {
    "id": 1,
    "name": "Lion",
    "type": "wild"
  },
  ....
  }
]*/

export interface VettAnimal {
  [animals: string]: Animal[]
}
export interface Animal {
  id: string;
  name: string;
  type: any;
}


