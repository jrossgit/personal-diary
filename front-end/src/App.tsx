import { useEffect, useState } from 'react'
import './App.css'
import type { ICategory, ICategorySummary, ITodo } from './utils/interfaces'
import { completeTodo, getCategories, getCategoryDetail } from './utils/http'

// TODOs
// Install typescript stubs as used in Hub
// Request in progress indicator

interface ITodoProps {
  todo: ITodo;  // TODO control via text
  onComplete: Function; // TODO more detailed type
}

function Todo({ todo, onComplete }: ITodoProps) {
  return <li>
    {todo.text}
    <button onClick={(_) => {onComplete()}}>✔</button>
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

  function onComplete(todoId: string) {
    completeTodo(todoId).then(
      (resp) => setTodos(todos.filter(t => t.id !== todoId))
    );
  }

  return (
  <>
    {
      category ? <>
        <h2>{category.name}</h2>
        {todos.length ? 
        <ul>
          {todos.map(todo => <Todo todo={todo} onComplete={() => onComplete(todo.id)}/>)}
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
