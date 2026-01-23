import { useEffect, useState } from 'react'
import './App.css'
import type { ICategory, ICategorySummary, ITodo } from './utils/interfaces'
import { completeTodo, createCategory, createTodo, deleteTodo, getCategories, getCategoryDetail } from './utils/http'

// TODOs
// Install typescript stubs as used in Hub
// Request in progress indicator


interface IInputComponentProps {
  onSubmit: Function; // TODO more detailed type
  initialText?: string;
}

function InputComponent({ onSubmit, initialText = "" }: IInputComponentProps) {

  const [text, setText] = useState(initialText);

  function submit(formData: any) {
      onSubmit(formData.get("text"));
  }

  return <form action={submit}>
    <input name="text" onChange={e => setText(e.target.value)}></input>
    <button type="submit">
      Submit
    </button>
  </form>
}

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

  function showInput() { setInputVisible(true); }

  return <>
    {
      inputVisible ? <InputComponent onSubmit={onCreate} />
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
        <div className="card">
        <h2>{category.name}</h2>
        <ul>
          {todos.map(todo => <Todo
            key={todo.id}
            todo={todo}
            onComplete={() => onComplete(todo.id)}
            onDelete={() => onDelete(todo.id)}
          />)}
          <InputTodo key={category.id} onCreate={onDoCreate}/>
        </ul>
        </div>
      :
      <h2>Select a category</h2>
    }
  </>
  )
}

interface INewCategoryFormProps {
  onCreate: Function;
}
function NewCategoryForm({ onCreate }: INewCategoryFormProps) {

  return <div className="card">
    <h2>Create New Category</h2>
    <InputComponent onSubmit={onCreate} />
  </div>
}


function App() {
  const [categories, setCategories] = useState<ICategorySummary[]>([]);
  const [newCategoryFormOpen, setNewCategoryFormOpen] = useState<boolean>(false)
  const [selectedCategory, setSelectedCategory] = useState<ICategorySummary | null>(null);

  useEffect(() => {
          getCategories()
          .then((data) => {
              setCategories(data);
          });
      }, [])

  function onCreateCategory(text: string) {

    createCategory(text).then(
      (resp) => {
        setCategories([resp, ...categories]);
        setSelectedCategory(resp);
        setNewCategoryFormOpen(false);
      }
    );
  }

  return (
    <>
      <header>
        <h1>Diary</h1>
      </header>
        <nav className="left-nav">
          <ul>
            <li key="newcategory" onClick={(_) => {setNewCategoryFormOpen(true)}}><button><strong>+ </strong>New Category</button></li>
            {categories.map(
              cat => <li key={cat.id}><a onClick={(e) => {setNewCategoryFormOpen(false); setSelectedCategory(cat);}}>{cat.name}</a></li>
            )}
          </ul>
        </nav>
        <main>
          {newCategoryFormOpen ?
            <NewCategoryForm onCreate={onCreateCategory} />
            :
            <CategoryCard category={selectedCategory}/>
          }
        </main>
    </>
  )
}

export default App
