<template>
  <div>
    <div class="p-4">
      <table class="table table-primary table-hover table-bordered table-responsive align-middle">
        <thead class="table-dark">
          <tr>
            <th>Book ID</th>
            <th>User Name</th>
            <th>Book Name</th>
            <th>Author</th>
            <th>Availability</th>
            <th>Issue Date</th>
            <th>Return Date</th>
            <th>Issue</th>
            <th>Revoke</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>{{ book.id }}</td>
            <td>{{ book.username }}</td>
            <td>{{ book.name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.availability }}</td>
            <td>{{ book.issueDate }}</td>
            <td>{{ book.returnDate }}</td>
            <td>
              <button
                v-if="book.status === 0 && book.availability > 0"
                @click="issueBook(book.id, book.username)"
                class="btn btn-light"
              >
                Issue Book
              </button>
              <button
                v-else
                type="button"
                disabled
                class="btn btn-light"
              >
                Issue Book
              </button>
            </td>
            <td>
              <button
                v-if="book.status === 1"
                @click="revokeBook(book.id, book.username)"
                class="btn btn-light"
              >
                Revoke Book
              </button>
              <button
                v-else
                type="button"
                disabled
                class="btn btn-light"
              >
                Revoke Book
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: [] // This will hold the book data
    };
  },
  created() {
    this.fetchBooks(); // Fetch books when component is created
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/getBooks'); // Adjust the URL to your API
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async issueBook(bookId, username) {
      try {
        const response = await axios.post('/issueBook', {
          bookid: bookId,
          user: username
        });
        if (response.status === 200) {
          console.log('Successfully Issued');
          this.fetchBooks(); // Refresh the book list
        }
      } catch (error) {
        console.error('Error issuing book:', error);
      }
    },
    async revokeBook(bookId, username) {
      try {
        const response = await axios.post('/revokeBook', {
          bookid: bookId,
          user: username
        });
        if (response.status === 200) {
          console.log('Successfully Revoked');
          this.fetchBooks(); // Refresh the book list
        }
      } catch (error) {
        console.error('Error revoking book:', error);
      }
    }
  }
};
</script>
