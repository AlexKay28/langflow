import React, {useState, useEffect} from 'react'
import api from "../../utils/api";
import CircularProgress from '@material-ui/core/CircularProgress';
import Box from '@material-ui/core/Box';
import './question.scss'

const Question = () => {
  const [question, setQuestion] = useState<string>('');
  const [question_token, setQuestionToken] = useState<string>('');
  const [user_answer, setUserAnswer] = useState<string>('');
  const [isAnswer, setIsAnswer] = useState<boolean>(false);
  const [answer, setAnswer] = useState<string>('');
  const [is_equal, setIsEqual] = useState<string>('');
  const [score, setScore] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    setTimeout(async () => {
      const questionConfig = {
        first_language: window.localStorage.getItem('firstLanguage'),
        second_language: window.localStorage.getItem('secondLanguage'),
        level: window.localStorage.getItem('level'),
      }
      const session_token = window.localStorage.getItem('session_token')
      const response: any = await api.post('/question', questionConfig, { headers: { session_token: `${session_token}` } })
      setQuestion(response.data.question)
      setQuestionToken(response.data.question_token)
    }, 100)
  }, [])

  const handleAnswerSubmit = async () => {  
    const data = {
        question_token: question_token,
        user_answer: user_answer
    }
    const session_token = window.localStorage.getItem('session_token')
    api.patch('/answer', data, { headers: { session_token: `${session_token}`}})
      .then((response: any) => {
        setAnswer(response.data.answer)
        setIsEqual(response.data.is_equal)
        setScore(response.data.score)
        setIsLoading(false)
      })
      .catch((error) => {
          console.log(error);
      });
    setIsAnswer(true)
  }

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target
    setUserAnswer(value)
  }

  const renderQuestion = (): JSX.Element => {    
    return (
      <div className="vh-100">
          <div className="centered-element">
              <h2>Translate: {question}</h2>
              <form onSubmit={handleAnswerSubmit}>
                  <div className="input-group mb-3">
                      <input 
                          type="string" 
                          className="form-control" 
                          placeholder="Enter text" 
                          autoComplete="off"
                          onChange={handleInputChange}
                      />
                      <div className="input-group-append">
                          <button className="btn btn-secondary" type="submit" onClick={handleAnswerSubmit}>Enter</button>
                      </div>
                  </div>
              </form>
          </div>
      </div>
    );
  }

  const renderAnswer = (): JSX.Element => {
    return (
      <div className="vh-100">
          <div className="centered-element w-100">
                { !isLoading ? 
                <table className="custom-table text-white-50">
                  <tbody>
                  <tr>
                      <td className="table-header">Translate:</td>
                      <td className="table-text table-text_translate">{question}</td>
                  </tr>
                  <tr>
                      <td className="table-header ">Answer:</td>
                      <td className="table-text table-text_answer">{user_answer}</td>
                  </tr>
                  <tr>
                      <td className="table-header">Correct answer:</td>
                      <td className="table-text table-text_correct-answer">{answer}</td>
                  </tr>
                  <tr>
                      <td className="table-header">Is equal:</td>
                      <td className="table-text table-text_correct-answer">{is_equal}</td>
                  </tr>
                  <tr>
                      <td className="table-header">Score:</td>
                      <td className="table-text table-text_correct-answer">{score}</td>
                  </tr>
                  </tbody>
              </table> : 
              renderSpinner()}
              <form>
                  <button className="btn btn-success btn-lg" value="Next"  id="next_button">Next</button>
              </form>
          </div>
      </div>
    );
  }

  const renderSpinner = (): JSX.Element => {
    return (
      <Box className="justify-content-center p-5" sx={{ display: 'flex' }}>
        <CircularProgress />
      </Box>
    );
  }
  
  return !isAnswer ? renderQuestion() : renderAnswer() 
}

export default Question