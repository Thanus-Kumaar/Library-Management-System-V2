<template>
  <div class="d-flex flex-column flex-lg-row" style="margin-top: 80px;">
    <div class="mt-4" style="width: 70%; height: fit-content;">
      <div class="text-light " style="font-size: 50px">
        Library Management System
      </div>
      <div class="text-light mt-4">
        Discover the ultimate solution for managing your library efficiently and
        effortlessly. Our Library Management System is designed to streamline
        the process of borrowing, returning, and managing books, making it easy
        for both librarians and patrons to stay organized.
      </div>
      <a href="">
        <button class="btn btn-secondary mt-4">
          Sign In to continue
        </button>
      </a>
    </div>
    <div
      class="d-flex flex-row flex-wrap justify-content-evenly"
      style="row-gap: 35px"
    >
      <div
        class="bg-secondary rounded p-3"
        style="width: 250px"
        v-for="feature in features"
      >
        <div class="h5 fst-italic fw-semibold" style="color: black;">{{ feature.title }}</div>
        <div style="font-size: 14px; color: black;">{{ feature.desc }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      features: [
        {
          title: "User-Friendly Interface",
          desc: "Navigate through a clean and intuitive interface that simplifies library management tasks. \
          Whether you're a librarian or a library member, our system is designed with you in mind.",
        },
        {
          title: "Efficient Book Management",
          desc: "Easily add, edit, and delete book records. Keep track of all your library's inventory \
          with detailed information on each book, including title, author, genre, and availability status.",
        },
        {
          title: "Seamless Borrowing and Returning",
          desc: "Our system allows patrons to borrow and return books with ease. Librarians can quickly \
          process transactions, reducing wait times and enhancing the user experience.",
        },
        {
          title: "Member Management",
          desc: "Manage member records efficiently. Keep track of who has borrowed what and when, and send\
           reminders for due dates. Membership renewal and registration are just a few clicks away.",
        },
        {
          title: "Search and Discover",
          desc: "Powerful search functionality helps users find books by title, author, genre, or keyword. \
          Advanced filtering options make discovering new reads easier than ever.",
        },
        {
          title: "Automated Notifications",
          desc: "Never miss a due date with automated email notifications for overdue books and upcoming due dates.\
           Keep members informed and reduce late returns.",
        },
      ],
    };
  },
};
</script>
