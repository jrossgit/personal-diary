import { useEffect, useRef, useState, type FormEvent } from 'react'
import './App.css'
import type { ICategory, ICategorySummary, ITodo } from './utils/interfaces'
import { completeTodo, createCategory, createTodo, deleteTodo, getCategories, getCategoryDetail, updateTodo } from './utils/http'

// TODOs
// Install typescript stubs as used in Hub
// Request in progress indicator


interface IInputComponentProps {
  onSubmit: Function; // TODO more detailed type
  initialText?: string;
}

function InputComponent({ onSubmit, initialText = "" }: IInputComponentProps) {

  function submit(formData: any) {
      onSubmit(formData.get("text"));
  }

  return <form action={submit}>
    <input name="text" defaultValue={initialText} required></input>
    <button type="submit">
      Submit
    </button>
  </form>
}


interface ITodoProps {
  todo?: ITodo;  // TODO control via text
  onComplete: Function; // TODO more detailed type
  onDelete: Function;
  onCreate: Function;  // TODO implement
  onUpdate: Function;
  initDisplayForm: boolean;
}
function TodoRow({ todo, onComplete, onDelete, onCreate, onUpdate, initDisplayForm }: ITodoProps) {

  const [displayForm, setDisplayForm] = useState<boolean>(initDisplayForm);

  const onSubmitInput = todo ? 
    (text: string) => {onUpdate(todo.id, text); setDisplayForm(false)}   // Use .then to handle failures?
    :
    onCreate
  
  return displayForm ? 
    <InputComponent onSubmit={onSubmitInput} initialText={todo ? todo.text : ""} />
    :
    <li>
      <span className={"clickable"} onDoubleClick={(_) => setDisplayForm(true)}>{todo.text}</span>
      <button onClick={(_) => {onComplete(todo.id)}}>✔</button>
      <button onClick={(_) => {onDelete(todo.id)}}>🗑</button>
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

  function onCreate(text: string) {
    const categoryId = category.id;

    createTodo(categoryId, text).then(
      (resp) => setTodos([...todos, resp])
    );
  }
  
  function onUpdate(todoId: string, text: string) {
    updateTodo(todoId, text).then(
      (resp) => setTodos(todos.map(t => t.id === todoId ? resp : t))
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
          {todos.map(todo => <TodoRow
            key={todo.id}
            todo={todo}
            onComplete={onComplete}
            onDelete={onDelete}
            onCreate={onCreate}
            onUpdate={onUpdate}
            initDisplayForm={false}
          />)}
          <TodoRow
            key="new"
            onComplete={onComplete}
            onDelete={onDelete}
            onCreate={onCreate}
            onUpdate={onUpdate}
            initDisplayForm={true}
          />
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
