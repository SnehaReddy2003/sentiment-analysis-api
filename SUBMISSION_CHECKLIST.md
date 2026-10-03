# Submission Checklist

- [ ] Push this project to a public GitHub repository.
- [ ] Run `pytest -q` and confirm tests pass.
- [ ] Run the API locally and verify `/docs`.
- [ ] Test `/api/analyze` with positive, negative and neutral examples.
- [ ] Test `/api/analyze/batch` with 10 texts.
- [ ] Test validation with 501 words and 11 batch items.
- [ ] Deploy to Render/Railway if a live URL is required.
- [ ] Add the live API URL to the GitHub README.
- [ ] If the evaluator specifically requires measured model accuracy, run a real
      held-out evaluation and add the measured metrics; do not invent metrics.
- [ ] If the company requires a training notebook, add one only if you choose
      the scikit-learn training route; this implementation uses a pretrained model.
