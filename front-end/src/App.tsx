import { useEffect, useState } from 'react'
import './App.css'
import type { ICategory, ICategorySummary, ITodo } from './utils/interfaces'
import { getCategories, getCategoryDetail } from './utils/http'

// TODOs
// Install typescript stubs as used in Hub

interface ITodoProps {
  todo: ITodo;
}

function Todo({ todo }: ITodoProps) {

  return <li>
    {todo.text}
    <button>✔</button>
    <button>🗑</button>
  </li>
}


interface ICategoryCardProps {
  category: ICategorySummary | null;
}

function CategoryCard({ category }: ICategoryCardProps ) {

  const [todos, setTodos] = useState<ITodo[]>([]);

  useEffect(() => {
    if (category) {
        getCategoryDetail(category.id)
        .then((data) => {
            setTodos(data);
        })
      }
    }, [category])

  return (
  <>
    {
      category ? <>
        <h2>{category.name}</h2>
        {todos.length ? 
        <ul>
          {todos.map(todo => <Todo todo={todo}/>)}
        </ul>
        : <p>Nothing to do!</p>}
      </>
      :
      <h2>Select a category</h2>
    }
  </>
  )
}


function App() {
  const [categories, setCategories] = useState<ICategorySummary[]>([])
  const [selectedCategory, setSelectedCategory] = useState<ICategorySummary | null>(null);

  useEffect(() => {
          getCategories()
          .then((data) => {
              setCategories(data);
          });
      }, [])

  return (
    <>
      <header>
        Header
      </header>
        <nav className="left-nav">
          <ul>
            {categories.map(
              cat => <a onClick={(e) => {setSelectedCategory(cat);}}><li>{cat.name}</li></a>
            )}
          </ul>
        </nav>
        <main>
          <CategoryCard category={selectedCategory}/>
        </main>

    </>
  )
}

export default App
