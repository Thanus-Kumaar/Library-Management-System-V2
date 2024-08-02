<template>
  <div>
    <div class="text-center pb-3" style="margin-top: 20px; font-size: 35px">
      Search Books
    </div>
    <div>
      <form @submit.prevent="searchBooks" class="row g-5 align-items-center justify-content-center">
        <div class="col-auto w-25">
          <label for="authorSearch" class="form-label">Search by author</label>
          <input 
            type="text" 
            class="form-control" 
            placeholder="Author Name" 
            v-model="searchCriteria.authorSearch"
            id="authorSearch" 
          />
        </div>
        <div class="col-auto w-25">
          <label for="bookSearch" class="form-label">Search by Book Name</label>
          <input 
            type="text" 
            class="form-control" 
            placeholder="Book Name" 
            v-model="searchCriteria.bookSearch"
            id="bookSearch" 
          />
        </div>
        <div class="col-auto w-25">
          <button 
            type="submit" 
            class="btn btn-primary mt-4 w-50 align-items-center"
          >
            Search
          </button>
        </div>
      </form>
    </div>
    <div class="p-4" v-if="books.length > 0">
      <table class="table table-primary table-hover table-bordered table-responsive">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Book Name</th>
            <th>Author</th>
            <th>Section</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>{{ book.id }}</td>
            <td>{{ book.name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.section }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center p-4">
      No results found.
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchCriteria: {
        authorSearch: '',
        bookSearch: ''
      },
      books: []
    };
  },
  methods: {
    searchBooks() {
      axios.post('http://127.0.0.1:5000/searchBooks', this.searchCriteria)
        .then(response => {
          this.books = response.data.books;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    }
  }
};
</script>