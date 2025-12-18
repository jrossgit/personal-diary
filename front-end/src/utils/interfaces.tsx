
export interface ITodoWrite {
    text: string;
}


export interface ITodo {
    id: string;
    text: string;
    categoryId: string;
    createTime: Date;   // TODO: Temporal?
}


export interface ICategorySummary {
    id: string;
    name: string;
    createTime: Date;   // TODO: Temporal?
}


export interface ICategory {
    id: string;
    name: string;
    createTime: Date;   // TODO: Temporal?   
    todos: ITodo[];
}
