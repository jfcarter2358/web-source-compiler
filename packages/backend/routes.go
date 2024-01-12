// routes.go

package main

import (
	"net/http"
	"scaffold/server/api"
	"scaffold/server/auth"
	"scaffold/server/config"
	"scaffold/server/constants"
	"scaffold/server/middleware"
	"scaffold/server/page"

	"github.com/gin-gonic/gin"
)

func initializeRoutes() {
	router.Static("/static/css", "./static/css")
	router.Static("/static/img", "./static/img")
	router.Static("/static/js", "./static/js")

	router.GET("/", page.RedirectIndexPage)

	router.NoRoute(func(c *gin.Context) {
		c.HTML(http.StatusNotFound, "404.html", gin.H{})
	})

	healthRoutes := router.Group("/health", middleware.CORSMiddleware())
	{
		healthRoutes.GET("/healthy", api.Healthy)
		healthRoutes.GET("/ready", api.Ready)
	}

	if config.Config.Node.Type == constants.NODE_TYPE_MANAGER {
		authRoutes := router.Group("/auth", middleware.CORSMiddleware())
		{
			// Add auth routes here
		}

		apiRoutes := router.Group("/api", middleware.CORSMiddleware())
		{
			v1Routes := apiRoutes.Group("/v1")
			{
				// Add API routes here
			}
		}

		uiRoutes := router.Group("/ui", middleware.CORSMiddleware())
		{
			// Add UI routes here
		}
	}
}
