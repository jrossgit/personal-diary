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


// export const postImages = (slug: string, rungNumber: number, submittedImages: number[]) => {
//     return fetch(`${API_BASE}/contests/${slug}/rungs/${rungNumber}/submit/`,
//     {
//         method: "POST",
//         headers: {
//             "Accept": "application/json",
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//             images: submittedImages
//         })
//     })
//     .then(
//         (response) => response.json())
//     .catch((err) => {
//         console.log(err.message);
//     })
// }
