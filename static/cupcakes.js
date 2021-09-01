const BASE_URL = 'http://localhost:5000/api/cupcakes'
const ul = document.querySelector('#cupcakes-list')
const addCupcakeBtn = document.querySelector('#new-cupcake-form button')
const cupcakeList = document.querySelector('#cupcakes-list')

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li class='cupcake-details'>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class='delete-button'>X</button>
      </li>
      <img class='Cupcake-img'
            src='${cupcake.image}'
            alt='(no image provided)'>
    </div>
  `
}

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}`)

  for (let cupcake of response.data.cupcakes) {
    let newCupcake = document.createElement('li')
    newCupcake.innerHTML = generateCupcakeHTML(cupcake)
    ul.append(newCupcake)
  }
}

async function addNewCupcake(flavor, size, rating, image) {
      const res = await axios.post(BASE_URL, {
        flavor: flavor.value,
        size: size.value,
        rating: rating.value,
        image: image.value 
      })
      
      let newCupcake = document.createElement('li')
      newCupcake.innerHTML = generateCupcakeHTML(res.data.cupcake)
      ul.append(newCupcake)
}

function resetForm(...inputs) {
  for (let input of inputs) {
    input.value = ''
  }
}

function handleNewCupcakeSubmittion(evt) {
  evt.preventDefault()

  let flavor = document.querySelector('#form-flavor')
  let size = document.querySelector('#form-size')
  let rating = document.querySelector('#form-rating')
  let image = document.querySelector('#form-image')

  addCupcake(flavor, size, rating, image)
  resetForm(flavor, size, rating, image)
}

async function deleteCupcake(target) {
  if (target.tagName === 'BUTTON') {
    let cupcakedetails = target.parentElement.parentElement
    let id = cupcakedetails.dataset.cupcakeId
    
    const res = await axios.delete(`${BASE_URL}/${id}`)

    cupcakedetails.parentElement.remove()
  }
}

showInitialCupcakes()

addCupcakeBtn.addEventListener('click', addNewCupcake)
cupcakeList.addEventListener('click', function(evt){deleteCupcake(evt.target)})