<template>
  <div>
    <div class="p-4">
      <h2 v-if="books.length == 0" class="text-center" style="margin-top: 100px;">
        No requests currently
      </h2>
      <table class="table table-primary table-hover table-bordered table-responsive align-middle" v-if="books.length != 0">
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
            <td>{{ book[0] }}</td>
            <td>{{ book[1] }}</td>
            <td>{{ book[2] }}</td>
            <td>{{ book[3] }}</td>
            <td>{{ book[4] }}</td>
            <td>{{ book[5] }}</td>
            <td>{{ book[6] }}</td>
            <td>
              <button
                v-if="book[7] === 0 && book[4] > 0"
                @click="issueBook(book[0], book[1])"
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
                v-if="book[7] === 1"
                @click="revokeBook(book[0], book[1])"
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
      books: []
    };
  },
  created() {
    this.fetchBooks();
    this.$checkUserRole("admin");
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/manageIssueRevoke');
        this.books = response.data.Books;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async issueBook(bookId, username) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/issueBook', {
          bookid: bookId,
          user: username
        });
        if (response.status === 200) {
          console.log('Successfully Issued');
          this.fetchBooks();
        }
      } catch (error) {
        console.error('Error issuing book:', error);
      }
    },
    async revokeBook(bookId, username) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/revokeBook', {
          bookid: bookId,
          user: username
        });
        if (response.status === 200) {
          console.log('Successfully Revoked');
          this.fetchBooks();
        }
      } catch (error) {
        console.error('Error revoking book:', error);
      }
    }
  }
};
</script>
