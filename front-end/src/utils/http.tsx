import type { ICategory, ICategorySummary, ITodo } from "./interfaces";

export const API_BASE = "http://localhost:8000";


export const getCategories = (): Promise<ICategorySummary[]> => {
    return fetch(`${API_BASE}/categories`)
    .then((response) => response.json())
    .catch((err) => {
        console.log(err.message);
    })
}


export const getCategoryDetail = (categoryId: string): Promise<ITodo[]> => {
    return fetch(`${API_BASE}/categories/${categoryId}/todos`)
    .then((response) => response.json())
    .catch((err) => {
        console.log(err.message);
    })
}


export const createTodo = (categoryId: string, text: string) => {
    return fetch(`${API_BASE}/categories/${categoryId}/todos`,
    {
        method: "POST",
        body: JSON.stringify({text: text}),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    })
    .then(
        (response) => response.json())
    .catch((err) => {
        console.log(err.message);
    })
}


export const completeTodo = (todoId: string) => {
    return fetch(`${API_BASE}/todos/${todoId}:complete`,
    {
        method: "POST",
    })
    .then(
        (response) => response.json())
    .catch((err) => {
        console.log(err.message);
    })
}


export const deleteTodo = (todoId: string) => {
    return fetch(`${API_BASE}/todos/${todoId}`,
    {
        method: "DELETE",
    })
    .then(
        (response) => response.json())
    .catch
    ((err) => {
        console.log(err.message);
    })
}


// export const getContestDetail = (slug: string): Promise<IContest> => {
//     return fetch(`${API_BASE}/contests/${slug}`)
//     .then((response) => response.json())
//     .catch((err) => {
//         console.log(err.message);
//     })
// }


// export const getRungList = (slug: string) => {
//     return fetch(`${API_BASE}/contests/${slug}/rungs`)
//     .then((response) => response.json())
//     .catch((err) => {
//         console.log(err.message);
//     })
// }
