using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Westwind.AspNetCore.Markdown;

namespace ZachWebSite
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.Configure<CookiePolicyOptions>(options =>
            {
                // This lambda determines whether user consent for non-essential cookies is needed for a given request.
                options.CheckConsentNeeded = context => false;
                options.MinimumSameSitePolicy = SameSiteMode.None;
            });

            services.AddRazorPages();
            services.AddMarkdown(config =>
            {
                // https://www.codemag.com/Article/1811071/Marking-up-the-Web-with-ASP.NET-Core-and-Markdown
                config.AddMarkdownProcessingFolder("/stories/");
            });
            // have to let MVC know we have a controller
            services.AddMvc(config =>
           {
               config.EnableEndpointRouting = false; // TBD: Figure out what this does.
           }

            ).AddApplicationPart(typeof(MarkdownPageProcessorMiddleware).Assembly);
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            app.UseDeveloperExceptionPage();
            app.UseHttpsRedirection();
            app.UseMarkdown();
            app.UseStaticFiles();
            app.UseCookiePolicy();
            app.UseRouting();
            app.UseMvc();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapRazorPages();
                endpoints.MapDefaultControllerRoute();
            });
        }
    }
}
