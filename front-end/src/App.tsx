import { useEffect, useState } from 'react'
import './App.css'
import type { ICategory, ICategorySummary, ITodo } from './utils/interfaces'
import { completeTodo, createTodo, deleteTodo, getCategories, getCategoryDetail } from './utils/http'

// TODOs
// Install typescript stubs as used in Hub
// Request in progress indicator

interface ITodoProps {
  todo: ITodo;  // TODO control via text
  onComplete: Function; // TODO more detailed type
  onDelete: Function;
}

function Todo({ todo, onComplete, onDelete }: ITodoProps) {
  return <li>
    {todo.text}
    <button onClick={(_) => {onComplete()}}>✔</button>
    <button onClick={(_) => {onDelete()}}>🗑</button>
  </li>
}

interface IInputTodoProps {
  onCreate: Function;
}
function InputTodo({ onCreate }: IInputTodoProps) {

  const [inputVisible, setInputVisible] = useState(false);
  const [text, setText] = useState("");

  function showInput() { setInputVisible(true); }

  return <>
    {
      inputVisible ? <>
        <input id="text" onChange={e => setText(e.target.value)}></input>
        <button onClick={(_) => {onCreate(text);}}>
          Submit
        </button>
      </>
      :
      <button onClick={showInput}><strong>+</strong></button>
    }
  </>
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

  function onDoCreate(text: string) {
    const categoryId = category.id;

    createTodo(categoryId, text).then(
      (resp) => setTodos([...todos, resp])
    );
  }

  function onComplete(todoId: string) {
    completeTodo(todoId).then(
      (resp) => setTodos(todos.filter(t => t.id !== todoId))
    );
  }

  function onDelete(todoId: string) {
    deleteTodo(todoId).then(
      (resp) => setTodos(todos.filter(t => t.id !== todoId))
    );
  }

  return (
  <>
    {
      category ?
      <>
        <h2>{category.name}</h2>
        <ul>
          {todos.map(todo => <Todo
            todo={todo}
            onComplete={() => onComplete(todo.id)}
            onDelete={() => onDelete(todo.id)}
          />)}
          <InputTodo onCreate={onDoCreate}/>
        </ul>
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
