SELECT *
FROM PortfolioProject..covidDeaths
WHERE continent is not null
order by 3,4

--SELECT *
--FROM PortfolioProject..covidVaccination
--order by 3,4

--Looking at the table information (data type)

--EXEC sp_help covidDeaths

-- Select the data we are going to use

SELECT Location, date, total_cases, new_cases, total_deaths, population
From PortfolioProject..covidDeaths
WHERE continent is not null
ORDER BY 1,2

-- Looking at Total Cases vs Total Dates
-- How many people got diagnosed actually die
-- Shows likelihood of dying if you contract covid in your country
SELECT Location, date, total_cases, total_deaths, (cast(total_deaths as float)/cast(total_cases as float))*100 as DeathPercentage
From PortfolioProject..covidDeaths
WHERE location like '%mexico%'
and continent is not null
ORDER BY 1,2

-- Looking at Total Cases vs Population
-- Shows what percentage of population got covid
SELECT Location, date, population, total_cases, (cast(total_cases as float)/cast(population as float))*100 as PercentPopulationInfected
From PortfolioProject..covidDeaths
--WHERE location like '%states%'
WHERE continent is not null
ORDER BY 1,2

-- Looking at Countries with Highest Infection Rate compared to Population
SELECT Location, population, MAX(total_cases) as HighestInfectionCount, MAX((cast(total_cases as float)/cast(population as float)))*100 as PercentPopulationInfected
From PortfolioProject..covidDeaths
GROUP BY location, population
ORDER BY PercentPopulationInfected desc

--Showing countries with Highest Death Count per Population
SELECT Location, MAX(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..covidDeaths
WHERE continent is not null
GROUP BY location
ORDER BY TotalDeathCount desc

-- Lets see by CONTINENT
-- Showing the continents with the highest death count per population
SELECT continent, MAX(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..covidDeaths
WHERE continent is not null
GROUP BY continent
ORDER BY TotalDeathCount desc


-- Lets break into GLOBAL

SELECT SUM(new_cases) as total_cases, SUM(CAST(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
From PortfolioProject..covidDeaths
--WHERE location like '%states%'
WHERE continent is not null
--and new_cases<>0
--GROUP BY date
ORDER BY 1,2


-- Looking at Total Population vs Vaccinations
WITH PopvsVac (Continent, Location, Date, Population,New_vaccinations, RollingPeopleVaccinated)
as 
(
SELECT dea.continent, dea.location, dea.date, dea.population,
vac.new_vaccinations, SUM(convert(bigint,vac.new_vaccinations)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM PortfolioProject..covidDeaths dea
JOIN PortfolioProject..covidVaccination vac
	ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)

SELECT *, (RollingPeopleVaccinated/Population)*100
FROM PopvsVac


-- TEMP TABLE
DROP TABLE IF EXISTS #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
RollingPeopleVaccinated numeric
)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population,
vac.new_vaccinations, SUM(convert(bigint,vac.new_vaccinations)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM PortfolioProject..covidDeaths dea
JOIN PortfolioProject..covidVaccination vac
	ON dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null
--order by 2,3

SELECT *, (RollingPeopleVaccinated/Population)*100
FROM #PercentPopulationVaccinated

-- CREATING VIEW TO STORE DATA FOR LATER VISUALIZATIONS

CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population,
vac.new_vaccinations, SUM(convert(bigint,vac.new_vaccinations)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM PortfolioProject..covidDeaths dea
JOIN PortfolioProject..covidVaccination vac
	ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

SELECT *
FROM PercentPopulationVaccinated