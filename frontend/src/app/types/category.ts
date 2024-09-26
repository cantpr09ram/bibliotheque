import { Book } from './book';
import { Event } from './event';

export type Category = {
    name: string;
    description: string;
    books: Book[];
    events: Event[];
  };