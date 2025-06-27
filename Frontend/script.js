document.addEventListener("DOMContentLoaded", () => {
  // Mobile Menu Toggle
  const mobileMenu = document.getElementById("mobile-menu")
  const mainMenu = document.getElementById("main-menu")

  mobileMenu.addEventListener("click", (e) => {
    e.stopPropagation()
    mobileMenu.classList.toggle("active")
    mainMenu.classList.toggle("active")
  })

  document.addEventListener("click", (e) => {
    if (!mainMenu.contains(e.target) && !mobileMenu.contains(e.target)) {
      mobileMenu.classList.remove("active")
      mainMenu.classList.remove("active")
    }
  })

  document.querySelectorAll(".menu a").forEach((item) => {
    item.addEventListener("click", () => {
      mobileMenu.classList.remove("active")
      mainMenu.classList.remove("active")
    })
  })

  // Navigation Active State
  const sections = document.querySelectorAll("section")
  const navLinks = document.querySelectorAll(".nav-link")

  window.addEventListener("scroll", () => {
    let current = ""
    sections.forEach((section) => {
      const sectionTop = section.offsetTop
      const sectionHeight = section.clientHeight
      if (pageYOffset >= sectionTop - 200) {
        current = section.getAttribute("id")
      }
    })

    navLinks.forEach((link) => {
      link.classList.remove("active")
      if (link.getAttribute("href").substring(1) === current) {
        link.classList.add("active")
      }
    })

    // Check which section is active and highlight corresponding footer link
    const footerLinks = document.querySelectorAll(".footer-links a")
    footerLinks.forEach((link) => {
      link.classList.remove("active-footer-link")
      if (link.getAttribute("href").substring(1) === current) {
        link.classList.add("active-footer-link")
      }
    })
  })

  // Chat Button Functionality
  const askAiButton = document.getElementById("askAiButton")
  const chatPopup = document.getElementById("chatPopup")
  const closeChat = document.getElementById("closeChat")
  const loadingOverlay = document.getElementById("loadingOverlay")

  askAiButton.addEventListener("click", () => {
    loadingOverlay.style.display = "flex"
    setTimeout(() => {
      loadingOverlay.style.display = "none"
      chatPopup.style.bottom = "0"
    }, 1500)
  })

  closeChat.addEventListener("click", () => {
    chatPopup.style.bottom = "-100%"
  })

  window.addEventListener("click", (e) => {
    if (e.target === chatPopup) chatPopup.style.bottom = "-100%"
  })

  // Feedback Form
  const feedbackForm = document.getElementById("feedbackForm")
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", async (e) => {
      e.preventDefault()
      const submitButton = feedbackForm.querySelector('button[type="submit"]')
      submitButton.disabled = true
      submitButton.textContent = "Sending..."

      try {
        const formData = new FormData(feedbackForm)
        const response = await fetch(feedbackForm.action, {
          method: "POST",
          body: formData,
          headers: { Accept: "application/json" },
        })

        if (response.ok) {
          alert("Thank you for your submission! We will get back to you soon.")
          feedbackForm.reset()
        } else {
          throw new Error("Failed to send feedback.")
        }
      } catch (error) {
        alert("Oops! Something went wrong. Please try again later.")
        console.error(error)
      } finally {
        submitButton.disabled = false
        submitButton.textContent = "Submit Request"
      }
    })
  }

  // Game Functionality
  const canvas = document.getElementById("gameCanvas")
  if (canvas) {
    const ctx = canvas.getContext("2d")
    const resetBtn = document.getElementById("resetBtn")
    const gameOverScreen = document.getElementById("gameOverScreen")
    const restartBtn = document.getElementById("restart")
    const exitBtn = document.getElementById("exit")
    let animationFrame
    let gameActive = false
    let hitSound

    // Try to load sound, but don't break if it fails
    try {
      
    } catch (e) {
      console.log("Sound could not be loaded, using silent fallback")
    }

    function setCanvasSize() {
      const containerWidth = canvas.parentElement.clientWidth
      canvas.width = containerWidth
      canvas.height = containerWidth * 0.75

      // Reset paddle and ball positions when canvas is resized
      if (gameActive) {
        paddle.x = canvas.width / 2 - paddle.width / 2
        paddle.y = canvas.height - 20
      }
    }

    setCanvasSize()
    window.addEventListener("resize", setCanvasSize)

    const paddle = {
      x: 0,
      y: 0,
      width: 100,
      height: 10,
      speed: 8,
    }

    const ball = {
      x: 0,
      y: 0,
      radius: 10,
      dx: 4,
      dy: -4,
      speed: 4,
    }

    let score = 0
    let highScore = localStorage.getItem("highScore") || 0
    document.getElementById("highScore").textContent = highScore

    function initGame() {
      paddle.x = canvas.width / 2 - paddle.width / 2
      paddle.y = canvas.height - 20
      ball.x = canvas.width / 2
      ball.y = canvas.height / 2
      ball.dx = ball.speed * (Math.random() > 0.5 ? 1 : -1)
      ball.dy = -ball.speed
      score = 0
      document.getElementById("score").textContent = score
      gameActive = true
    }

    function drawPaddle() {
      ctx.fillStyle = "#fff"
      ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height)

      // Add a gradient effect to the paddle
      const gradient = ctx.createLinearGradient(paddle.x, paddle.y, paddle.x, paddle.y + paddle.height)
      gradient.addColorStop(0, "rgba(255, 111, 97, 0.8)")
      gradient.addColorStop(1, "rgba(255, 51, 102, 0.8)")
      ctx.fillStyle = gradient
      ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height)
    }

    function drawBall() {
      // Add a glow effect
      ctx.shadowColor = "rgba(255, 111, 97, 0.8)"
      ctx.shadowBlur = 15

      // Create gradient for ball
      const gradient = ctx.createRadialGradient(ball.x, ball.y, 0, ball.x, ball.y, ball.radius)
      gradient.addColorStop(0, "#ffffff")
      gradient.addColorStop(1, "rgba(255, 111, 97, 0.8)")

      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2)
      ctx.fill()

      // Reset shadow
      ctx.shadowBlur = 0
    }

    function update() {
      if (!gameActive) return

      ball.x += ball.dx
      ball.y += ball.dy

      // Wall collision
      if (ball.x - ball.radius < 0 || ball.x + ball.radius > canvas.width) {
        ball.dx *= -1
        try {
          if (hitSound) hitSound.play()
        } catch (e) {}
      }

      if (ball.y - ball.radius < 0) {
        ball.dy *= -1
        try {
          if (hitSound) hitSound.play()
        } catch (e) {}
      }

      // Paddle collision
      if (
        ball.y + ball.radius >= paddle.y &&
        ball.y + ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width
      ) {
        // Calculate bounce angle based on where the ball hits the paddle
        const hitPosition = (ball.x - paddle.x) / paddle.width
        const bounceAngle = hitPosition * Math.PI - Math.PI / 2

        const speed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy)
        ball.dx = speed * Math.cos(bounceAngle)
        ball.dy = -speed * Math.sin(bounceAngle)

        score++
        document.getElementById("score").textContent = score

        try {
          if (hitSound) hitSound.play()
        } catch (e) {}

        // Increase difficulty
        if (score % 5 === 0) {
          const newSpeed = Math.min(ball.speed * 1.05, 12) // Cap max speed
          ball.speed = newSpeed
          const currentDirection = { x: ball.dx > 0 ? 1 : -1, y: ball.dy > 0 ? 1 : -1 }
          ball.dx = newSpeed * 0.8 * currentDirection.x
          ball.dy = newSpeed * currentDirection.y
        }

        if (score > highScore) {
          highScore = score
          localStorage.setItem("highScore", highScore)
          document.getElementById("highScore").textContent = highScore
        }
      }

      // Game over
      if (ball.y + ball.radius > canvas.height) {
        gameOver()
      }

      // Keep paddle within canvas
      paddle.x = Math.max(0, Math.min(paddle.x, canvas.width - paddle.width))
    }

    function gameOver() {
      gameActive = false
      document.getElementById("finalScore").textContent = score
      gameOverScreen.style.display = "block"
      cancelAnimationFrame(animationFrame)
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Draw background grid
      ctx.strokeStyle = "rgba(255, 255, 255, 0.05)"
      ctx.lineWidth = 1
      const gridSize = 20

      for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas.height)
        ctx.stroke()
      }

      for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(canvas.width, y)
        ctx.stroke()
      }

      drawPaddle()
      drawBall()
      update()

      if (gameActive) {
        animationFrame = requestAnimationFrame(draw)
      }
    }

    // Mouse and touch controls
    canvas.addEventListener("mousemove", (e) => {
      if (!gameActive) return
      const rect = canvas.getBoundingClientRect()
      paddle.x = e.clientX - rect.left - paddle.width / 2
    })

    canvas.addEventListener("touchmove", (e) => {
      if (!gameActive) return
      e.preventDefault()
      const rect = canvas.getBoundingClientRect()
      const touchX = e.touches[0].clientX
      paddle.x = touchX - rect.left - paddle.width / 2
    })

    // Keyboard controls
    window.addEventListener("keydown", (e) => {
      if (!gameActive) return

      if (e.key === "ArrowLeft" || e.key === "a") {
        paddle.x -= paddle.speed * 2
      } else if (e.key === "ArrowRight" || e.key === "d") {
        paddle.x += paddle.speed * 2
      }

      // Keep paddle within canvas
      paddle.x = Math.max(0, Math.min(paddle.x, canvas.width - paddle.width))
    })

    // Game buttons
    resetBtn.addEventListener("click", () => {
      gameOverScreen.style.display = "none"
      initGame()
      draw()
    })

    if (restartBtn) {
      restartBtn.addEventListener("click", () => {
        gameOverScreen.style.display = "none"
        initGame()
        draw()
      })
    }

    if (exitBtn) {
      exitBtn.addEventListener("click", () => {
        gameOverScreen.style.display = "none"
        gameActive = false
        cancelAnimationFrame(animationFrame)
        window.location.href = "#home"
      })
    }

    // Start game on canvas click
    canvas.addEventListener("click", () => {
      if (!gameActive) {
        gameOverScreen.style.display = "none"
        initGame()
        draw()
      }
    })

    // Initialize game when section becomes visible
    const gameSection = document.getElementById("game")
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !gameActive) {
            initGame()
            draw()
          }
        })
      },
      { threshold: 0.5 },
    )

    if (gameSection) {
      observer.observe(gameSection)
    }
  }

  // Blog functionality
  const blogCategories = document.querySelectorAll(".blog-category")
  const readMoreLinks = document.querySelectorAll(".read-more")

  blogCategories.forEach((category) => {
    category.addEventListener("click", () => {
      // This would link to the full category page
      // For now just add a visual feedback
      category.classList.add("active")
      setTimeout(() => category.classList.remove("active"), 300)
    })
  })

  readMoreLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      // This would open the full post
      // For now just add a visual feedback
      const postItem = link.closest(".post-item")
      postItem.classList.add("active")
      setTimeout(() => postItem.classList.remove("active"), 300)
    })
  })

  // Tool links functionality
  const toolLinks = document.querySelectorAll(".tool-link:not(.disabled)")
  toolLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      // Add visual feedback before navigating
      const toolCard = link.closest(".tool-card")
      if (toolCard) {
        toolCard.classList.add("active")
      }
    })
  })

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href")
      if (targetId === "#") return

      const targetElement = document.querySelector(targetId)
      if (targetElement) {
        // Get header height for offset
        const headerHeight = document.querySelector("header").offsetHeight

        window.scrollTo({
          top: targetElement.offsetTop - headerHeight,
          behavior: "smooth",
        })

        // Update URL without scrolling
        history.pushState(null, null, targetId)
      }
    })
  })

  // Reveal animations on scroll
  const revealElements = document.querySelectorAll(".section, .feature-card, .blog-category, .post-item, .tool-card")

  const revealOnScroll = () => {
    revealElements.forEach((element) => {
      const elementTop = element.getBoundingClientRect().top
      const windowHeight = window.innerHeight

      if (elementTop < windowHeight - 100) {
        element.classList.add("revealed")
      }
    })
  }

  // Initial setup for reveal animations
  revealElements.forEach((element) => {
    element.classList.add("reveal-element")
  })

  window.addEventListener("scroll", revealOnScroll)
  revealOnScroll() // Check on initial load

  // Handle window resize events
  let resizeTimer
  window.addEventListener("resize", () => {
    // Debounce resize events
    clearTimeout(resizeTimer)
    resizeTimer = setTimeout(() => {
      // Adjust any elements that need resizing
      if (canvas && typeof window.setCanvasSize === "function") {
        window.setCanvasSize()
      }

      // Check for mobile vs desktop view
      if (window.innerWidth > 768) {
        if (mainMenu) mainMenu.style.right = ""
      }
    }, 250)
  })

  // Preload images for better performance
  const preloadImages = () => {
    const images = document.querySelectorAll("img")
    images.forEach((img) => {
      const src = img.getAttribute("src")
      if (src) {
        const newImg = new Image()
        newImg.src = src
      }
    })
  }

  preloadImages()
})
