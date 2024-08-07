<template>
  <div>
    <object
      v-if="pdfUrl"
      :data="pdfUrl"
      type="application/pdf"
      style="width: 100%; height: 100%;"
      width="800"
      height="600"
    >
      <p>Your browser does not support PDFs. <a :href="pdfUrl">Download the PDF</a>.</p>
    </object>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PdfViewer',
  data() {
    return {
      pdfUrl: null,
    };
  },
  created() {
    this.loadPdf();
  },
  methods: {
    async loadPdf() {
      const filename = this.$route.query.filename;
      if (filename) {
        try {
          const response = await axios.get(`/view-file?filename=${filename}`, {
            responseType: 'blob', // Important for handling binary data
          });
          const url = window.URL.createObjectURL(new Blob([response.data]));
          this.pdfUrl = url;
        } catch (error) {
          console.error('Error loading PDF:', error);
        }
      }
    }
  }
};
</script>